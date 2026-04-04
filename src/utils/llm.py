"""LLM client — thin wrapper around the OpenRouter chat completions API.

Uses only stdlib (urllib + json + threading + time) — no extra dependencies.

Exports
-------
LLMResult      : dataclass returned by every successful call
LLMSignals     : QObject subclass with result/error pyqtSignals (thread-safe bridge)
LLMClient      : the actual HTTP client
CouncilResult  : dataclass returned by a council run
LLMCouncil     : fan-out client that queries multiple models and synthesises
load_llm_client / save_llm_config          : single-model config helpers
load_council_config / save_council_config  : council config helpers
DEFAULT_MODEL  : fallback model string
"""

from __future__ import annotations

import json
import logging
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Callable

from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger(__name__)

OPENROUTER_BASE = "https://openrouter.ai/api/v1"
DEFAULT_MODEL   = "qwen/qwen3-6b-plus:free"

COUNCIL_SYNTHESIS_MODES = ["Consensus", "Best Pick", "Debate"]
DEFAULT_SYNTHESIS_MODE  = "Consensus"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Result dataclasses
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


@dataclass
class CouncilResult:
    """Returned by a successful LLMCouncil run.

    Attributes
    ----------
    final           : The synthesised LLMResult produced by the synthesis pass.
    members         : One LLMResult per council model that responded successfully.
    failed_models   : Model IDs that errored out during the fan-out phase.
    synthesis_model : The model used for the final synthesis pass.
    synthesis_mode  : One of 'Consensus', 'Best Pick', 'Debate'.
    """
    final:           LLMResult
    members:         list[LLMResult]          = field(default_factory=list)
    failed_models:   list[str]                = field(default_factory=list)
    synthesis_model: str                      = ""
    synthesis_mode:  str                      = DEFAULT_SYNTHESIS_MODE

    @property
    def member_count(self) -> int:
        return len(self.members)

    def summary(self) -> str:
        ok  = self.member_count
        err = len(self.failed_models)
        parts = [f"{ok} member{'s' if ok != 1 else ''} responded"]
        if err:
            parts.append(f"{err} failed")
        parts.append(self.final.timing_summary())
        return " · ".join(parts)


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


class CouncilSignals(QObject):
    """Same pattern as LLMSignals but for CouncilResult."""
    result = pyqtSignal(object)   # carries CouncilResult
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

        if text is None:
            # Some models (e.g. reasoning/thinking models) return null content.
            # Treat as an error so the council marks this member as failed
            # rather than creating a malformed result that crashes synthesis.
            raise RuntimeError(
                f"Model returned null content — response: {json.dumps(data)[:200]}"
            )

        usage = data.get("usage") or {}

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
#  Council
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_SYNTHESIS_PROMPTS: dict[str, str] = {
    "Consensus": (
        "You are a synthesis engine. Below are responses from {n} different AI models "
        "to the same question. Your task is to identify the common ground, reconcile "
        "any differences, and produce a single coherent answer that represents the "
        "best consensus. Do not mention the individual models or that this is a synthesis.\n\n"
        "{responses}\n\nProvide the synthesised answer:"
    ),
    "Best Pick": (
        "You are a quality judge. Below are responses from {n} different AI models "
        "to the same question. Select the single most accurate, well-reasoned, and "
        "complete response. You may lightly polish it, but preserve its core content. "
        "Do not mention the selection process.\n\n"
        "{responses}\n\nProvide the best response:"
    ),
    "Debate": (
        "You are a deliberation moderator. Below are responses from {n} different AI "
        "models that may agree or disagree with each other. Analyse the strongest "
        "arguments from each side and produce a final, balanced conclusion that "
        "acknowledges key tensions where they exist.\n\n"
        "{responses}\n\nProvide the final conclusion:"
    ),
}


class LLMCouncil:
    """Queries multiple OpenRouter models in parallel and synthesises their responses.

    Parameters
    ----------
    api_key         : OpenRouter API key (shared across all members).
    council_models  : List of 3–6 model ID strings.
    synthesis_model : Model used for the synthesis pass (defaults to council_models[0]).
    synthesis_mode  : One of 'Consensus', 'Best Pick', 'Debate'.
    timeout         : Per-request timeout in seconds.
    """

    MAX_MEMBERS = 6
    MIN_MEMBERS = 3

    def __init__(
        self,
        api_key:         str,
        council_models:  list[str],
        synthesis_model: str  = "",
        synthesis_mode:  str  = DEFAULT_SYNTHESIS_MODE,
        timeout:         int  = 90,
    ):
        if not council_models:
            raise ValueError("council_models must contain at least one model ID.")
        self.api_key         = api_key.strip()
        self.council_models  = council_models[: self.MAX_MEMBERS]
        self.synthesis_model = (synthesis_model.strip() or self.council_models[0])
        self.synthesis_mode  = synthesis_mode if synthesis_mode in COUNCIL_SYNTHESIS_MODES \
                               else DEFAULT_SYNTHESIS_MODE
        self.timeout         = timeout

    # ── Internal helpers ────────────────────────────────────────────────────

    def _client(self, model: str) -> LLMClient:
        return LLMClient(api_key=self.api_key, model=model, timeout=self.timeout)

    def _call_member(
        self,
        model:       str,
        messages:    list[dict],
        max_tokens:  int,
        temperature: float,
    ) -> tuple[str, LLMResult | None, str]:
        """Call one council member.  Returns (model, result_or_None, error_str)."""
        try:
            result = self._client(model).complete(messages, max_tokens, temperature)
            return model, result, ""
        except Exception as exc:
            logger.warning("Council member %s failed: %s", model, exc)
            return model, None, str(exc)

    def _build_synthesis_messages(
        self,
        original_messages: list[dict],
        member_results:    list[LLMResult],
    ) -> list[dict]:
        """Build the synthesis prompt incorporating all member responses."""
        # Re-state the original user question
        user_question = ""
        for m in original_messages:
            if m.get("role") == "user":
                user_question = m.get("content", "")
                break

        response_blocks = "\n\n".join(
            f"--- Model {i + 1} ({r.model.split('/')[-1].replace(':free','').replace(':nitro','')}) ---\n{(r.text or '').strip()}"
            for i, r in enumerate(member_results)
        )

        template = _SYNTHESIS_PROMPTS.get(self.synthesis_mode,
                                          _SYNTHESIS_PROMPTS[DEFAULT_SYNTHESIS_MODE])
        synthesis_prompt = template.format(
            n=len(member_results),
            responses=response_blocks,
        )

        messages = []
        if user_question:
            messages.append({
                "role": "user",
                "content": f"Original question: {user_question}",
            })
            messages.append({
                "role": "assistant",
                "content": "I have received the individual responses and will now synthesise them.",
            })
        messages.append({"role": "user", "content": synthesis_prompt})
        return messages

    # ── Public API ──────────────────────────────────────────────────────────

    def complete(
        self,
        messages:    list[dict],
        max_tokens:  int   = 1200,
        temperature: float = 0.4,
    ) -> CouncilResult:
        """Synchronous council call — blocks until all members and synthesis finish.

        Fan-out is parallel; synthesis is sequential after fan-out completes.
        Always run from a worker thread.
        """
        member_results: list[LLMResult] = []
        failed_models:  list[str]       = []

        # ── Fan-out phase ──────────────────────────────────────────────────
        with ThreadPoolExecutor(max_workers=len(self.council_models)) as pool:
            futures = {
                pool.submit(self._call_member, model, messages, max_tokens, temperature): model
                for model in self.council_models
            }
            for future in as_completed(futures):
                model, result, err = future.result()
                if result is not None:
                    member_results.append(result)
                else:
                    failed_models.append(model)

        if not member_results:
            raise RuntimeError(
                f"All {len(self.council_models)} council members failed. "
                f"Last errors: {', '.join(failed_models)}"
            )

        # Sort member results to match original council_models order for stable display
        order = {m: i for i, m in enumerate(self.council_models)}
        member_results.sort(key=lambda r: order.get(r.model, 999))

        # ── Synthesis phase ────────────────────────────────────────────────
        if len(member_results) == 1:
            # Only one member responded — skip synthesis, return it directly
            final = member_results[0]
        else:
            synth_messages = self._build_synthesis_messages(messages, member_results)
            synth_max      = min(max_tokens, 1200)
            final = self._client(self.synthesis_model).complete(
                synth_messages, synth_max, temperature
            )

        return CouncilResult(
            final           = final,
            members         = member_results,
            failed_models   = failed_models,
            synthesis_model = self.synthesis_model,
            synthesis_mode  = self.synthesis_mode,
        )

    def complete_async(
        self,
        messages:    list[dict],
        on_result:   Callable[[CouncilResult], None],
        on_error:    Callable[[str],           None],
        max_tokens:  int   = 1200,
        temperature: float = 0.4,
    ) -> None:
        """Non-blocking council call — fires a single daemon thread."""
        def _worker():
            try:
                result = self.complete(messages, max_tokens, temperature)
                on_result(result)
            except Exception as exc:
                logger.warning("LLMCouncil async failed: %s", exc)
                on_error(str(exc))

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


def load_council_config() -> "LLMCouncil | None":
    """Return a configured LLMCouncil, or None if council is disabled / unconfigured."""
    from src.config import load_config
    cfg = load_config()
    if not cfg.get("council_enabled", False):
        return None
    key    = cfg.get("openrouter_api_key", "").strip()
    models = cfg.get("council_models", [])
    if not key or not models:
        return None
    return LLMCouncil(
        api_key         = key,
        council_models  = models,
        synthesis_model = cfg.get("council_synthesis_model", "").strip(),
        synthesis_mode  = cfg.get("council_synthesis_mode",  DEFAULT_SYNTHESIS_MODE),
    )


def save_council_config(
    enabled:          bool,
    models:           list[str],
    synthesis_model:  str,
    synthesis_mode:   str,
) -> None:
    """Persist council settings to config."""
    from src.config import load_config, save_config
    cfg = load_config()
    cfg["council_enabled"]          = enabled
    cfg["council_models"]           = [m.strip() for m in models if m.strip()]
    cfg["council_synthesis_model"]  = synthesis_model.strip()
    cfg["council_synthesis_mode"]   = synthesis_mode
    save_config(cfg)