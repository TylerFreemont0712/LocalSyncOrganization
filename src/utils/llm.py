"""LLM client — thin wrapper around the OpenRouter chat completions API.

Uses only stdlib (urllib + json + threading + time) — no extra dependencies.

Exports
-------
LLMResult   : dataclass returned by every successful call
LLMSignals  : QObject subclass with result/error pyqtSignals (thread-safe bridge)
LLMClient   : the actual HTTP client
load_llm_client / save_llm_config : config helpers
DEFAULT_MODEL : fallback model string
"""

from __future__ import annotations

import json
import logging
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)

OPENROUTER_BASE = "https://openrouter.ai/api/v1"
DEFAULT_MODEL   = "qwen/qwen3-6b-plus:free"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Result dataclass
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class LLMResult:
    """Returned by every successful LLM call."""
    text:              str
    elapsed_ms:        int
    model:             str
    prompt_tokens:     int = 0
    completion_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    @property
    def elapsed_s(self) -> float:
        return self.elapsed_ms / 1000

    def timing_summary(self) -> str:
        parts = [f"{self.elapsed_s:.1f}s"]
        if self.total_tokens:
            parts.append(
                f"{self.total_tokens} tokens"
                f" ({self.prompt_tokens}↑ {self.completion_tokens}↓)"
            )
        if self.model:
            short = self.model.split("/")[-1].replace(":free", "").replace(":nitro", "")
            parts.append(short)
        return " · ".join(parts)

    def __str__(self) -> str:
        return self.text


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Thread-safe signal bridge  (shared by all UI components)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LLMSignals(QObject):
    """QObject whose signals marshal LLM callbacks onto the Qt main thread.

    Always store an instance on *self* (not a local variable) so the
    underlying C++ object is not garbage-collected before the worker
    thread fires.
    """
    result = pyqtSignal(object)   # carries LLMResult
    error  = pyqtSignal(str)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Client
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LLMClient:
    """Thin OpenRouter chat-completions client."""

    def __init__(self, api_key: str,
                 model:   str = DEFAULT_MODEL,
                 timeout: int = 60):
        self.api_key = api_key.strip()
        self.model   = model.strip()
        self.timeout = timeout

    def complete(self, messages: list[dict],
                 max_tokens:   int   = 1200,
                 temperature:  float = 0.4) -> LLMResult:
        """Synchronous call — blocks. Use only from a worker thread."""
        payload = json.dumps({
            "model":       self.model,
            "messages":    messages,
            "max_tokens":  max_tokens,
            "temperature": temperature,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{OPENROUTER_BASE}/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type":  "application/json",
                "HTTP-Referer":  "https://localsync.app",
                "X-Title":       "LocalSync",
            },
            method="POST",
        )

        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            try:
                msg = json.loads(body).get("error", {}).get("message", body)
            except Exception:
                msg = body
            raise RuntimeError(f"OpenRouter API error {exc.code}: {msg}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Network error: {exc.reason}") from exc
        elapsed_ms = int((time.perf_counter() - t0) * 1000)

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON response: {raw[:120]}") from exc

        try:
            text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise RuntimeError(
                f"Unexpected response schema: {json.dumps(data)[:200]}"
            ) from exc

        usage = data.get("usage") or {}
        model = data.get("model") or self.model
        return LLMResult(
            text              = text,
            elapsed_ms        = elapsed_ms,
            model             = model,
            prompt_tokens     = usage.get("prompt_tokens",     0),
            completion_tokens = usage.get("completion_tokens", 0),
        )

    def complete_async(
        self,
        messages:    list[dict],
        on_result:   Callable[[LLMResult], None],
        on_error:    Callable[[str],       None],
        max_tokens:  int   = 1200,
        temperature: float = 0.4,
        retries:     int   = 3,
    ) -> None:
        """Non-blocking — fires a daemon thread.  Retries on 429 with back-off."""
        def _worker():
            last_err = ""
            for attempt in range(max(retries, 1)):
                try:
                    result = self.complete(messages, max_tokens, temperature)
                    on_result(result)
                    return
                except RuntimeError as exc:
                    last_err = str(exc)
                    if "429" in last_err and attempt < retries - 1:
                        wait = 4 * (attempt + 1)
                        logger.info("LLM 429 — retrying in %ss (%d/%d)",
                                    wait, attempt + 1, retries)
                        time.sleep(wait)
                    else:
                        break
                except Exception as exc:
                    last_err = str(exc)
                    break
            logger.warning("LLM call failed after %d attempt(s): %s", retries, last_err)
            on_error(last_err)

        threading.Thread(target=_worker, daemon=True).start()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Config helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_llm_client() -> "LLMClient | None":
    """Return a configured LLMClient, or None if no key is saved."""
    from src.config import load_config
    cfg   = load_config()
    key   = cfg.get("openrouter_api_key", "").strip()
    model = cfg.get("openrouter_model",   DEFAULT_MODEL).strip() or DEFAULT_MODEL
    return LLMClient(api_key=key, model=model) if key else None


def save_llm_config(api_key: str, model: str) -> None:
    """Persist API key and model choice to config."""
    from src.config import load_config, save_config
    cfg = load_config()
    cfg["openrouter_api_key"] = api_key.strip()
    cfg["openrouter_model"]   = model.strip() or DEFAULT_MODEL
    save_config(cfg)