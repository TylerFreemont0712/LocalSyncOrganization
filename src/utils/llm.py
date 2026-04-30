"""LLM client — llama.cpp server backend with lightweight multi-pass council.

Uses only stdlib (urllib + json + threading) — no extra dependencies.

The llama.cpp server exposes an OpenAI-compatible /v1/chat/completions endpoint.
No model selection is needed — the model is locked server-side.

Exports
-------
LLMResult       : dataclass returned by every successful call
LLMSignals      : QObject with result/error pyqtSignals (thread-safe bridge)
LLMClient       : thin /v1/chat/completions client
CouncilResult   : dataclass returned by a multi-pass council run
CouncilSignals  : QObject with result/error pyqtSignals for council
LightCouncil    : 3-pass council (Precise / Balanced / Creative) + synthesis
LLMCouncil      : alias for LightCouncil (backwards compat)
load_llm_client       : config helper → LLMClient
load_council_config   : config helper → LightCouncil | None
save_llm_config       : persist host to config
save_council_config   : persist council enabled flag + mode + concurrency
LLAMA_DEFAULT_HOST    : default server URL
COUNCIL_SYNTHESIS_MODES : list of available council modes for the UI
COUNCIL_MODE_DELIBERATE : N parallel passes + synthesis call (richer, slower)
COUNCIL_MODE_QUICK      : N parallel passes, longest non-empty wins (faster)
COUNCIL_DEFAULT_CONCURRENCY : default number of parallel in-flight requests

v0.8.0 — Async, progressive council
───────────────────────────────────
  • CouncilSignals now emits a `member_started` and `member_completed` signal
    as each pass kicks off / returns, so the UI can paint cards live instead
    of waiting for the slowest pass.
  • A module-level Semaphore (`_REQUEST_SLOTS`) caps concurrent in-flight
    completions across the entire app to match the llama.cpp server's
    configured parallelism — set via `set_request_concurrency()` or the
    `council_concurrency` config key (default: COUNCIL_DEFAULT_CONCURRENCY).
  • LightCouncil schedules synthesis as soon as all members complete and
    runs it through the same semaphore, so a long-running council from one
    panel cannot starve a chat call from another.
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

# ── Server defaults ────────────────────────────────────────────────────────────
LLAMA_DEFAULT_HOST  = "http://192.168.0.30:8080"
# Legacy alias — any code that still references OLLAMA_DEFAULT_HOST will not break
OLLAMA_DEFAULT_HOST = LLAMA_DEFAULT_HOST
DEFAULT_MODEL       = ""   # model is server-side; kept for legacy compat only

# ── Council modes ─────────────────────────────────────────────────────────────
COUNCIL_MODE_DELIBERATE = "Deliberate"
COUNCIL_MODE_QUICK      = "Quick"
COUNCIL_SYNTHESIS_MODES = [COUNCIL_MODE_DELIBERATE, COUNCIL_MODE_QUICK]
COUNCIL_DEFAULT_MODE    = COUNCIL_MODE_DELIBERATE

# ── Server concurrency ────────────────────────────────────────────────────────
# llama.cpp servers are typically configured for 2-3 in-flight slots
# (the `--parallel` flag). Cap the whole app to that many concurrent
# completions so a council burst from one panel cannot starve another.
COUNCIL_DEFAULT_CONCURRENCY = 3
_REQUEST_SLOTS = threading.BoundedSemaphore(COUNCIL_DEFAULT_CONCURRENCY)
_CURRENT_CONCURRENCY = COUNCIL_DEFAULT_CONCURRENCY


def set_request_concurrency(n: int) -> None:
    """Reset the global request semaphore to allow `n` simultaneous calls.

    Safe to call at any time — pending requests already inside the semaphore
    will continue to use the previous slot count until they release.
    """
    global _REQUEST_SLOTS, _CURRENT_CONCURRENCY
    n = max(1, min(int(n), 16))
    if n == _CURRENT_CONCURRENCY:
        return
    _REQUEST_SLOTS = threading.BoundedSemaphore(n)
    _CURRENT_CONCURRENCY = n


def get_request_concurrency() -> int:
    return _CURRENT_CONCURRENCY

# ── Council pass definitions: (name, temperature, system_prompt) ──────────────
COUNCIL_PASSES: list[tuple[str, float, str]] = [
    (
        "Precise",
        0.2,
        "You are a precise, analytical assistant. "
        "Respond with factual, well-structured, and concise information. "
        "Prioritise accuracy over creativity.",
    ),
    (
        "Balanced",
        0.6,
        "You are a balanced, thorough assistant. "
        "Provide well-reasoned, comprehensive responses that cover multiple angles.",
    ),
    (
        "Creative",
        1.0,
        "You are a creative, lateral-thinking assistant. "
        "Explore unconventional angles, fresh perspectives, and novel approaches.",
    ),
]
SYNTHESIS_TEMPERATURE = 0.4


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Dataclasses
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class LLMResult:
    """Returned by every successful LLM call."""
    text:       str
    model:      str = ""
    elapsed_ms: int = 0
    tokens_in:  int = 0
    tokens_out: int = 0

    def timing_summary(self) -> str:
        parts = [f"{self.elapsed_ms / 1000:.1f}s"]
        total = self.tokens_in + self.tokens_out
        if total:
            parts.append(f"{total} tok ({self.tokens_in}↑ {self.tokens_out}↓)")
        if self.model:
            parts.append(self.model.split("/")[-1])
        return " · ".join(parts)


@dataclass
class CouncilResult:
    """Returned by a successful LightCouncil run."""
    members: list[LLMResult] = field(default_factory=list)
    final:   LLMResult       = field(default_factory=lambda: LLMResult(text=""))
    failed:  list[str]       = field(default_factory=list)
    mode:    str             = COUNCIL_DEFAULT_MODE

    def summary(self) -> str:
        ok  = len(self.members)
        bad = len(self.failed)
        base = f"{ok} passes OK" + (f", {bad} failed" if bad else "")
        return f"{base} · {self.mode}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Qt signal bridges
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LLMSignals(QObject):
    """QObject whose signals marshal LLM callbacks onto the Qt main thread.

    Always store an instance on *self* (not a local variable) so the
    underlying C++ object is not garbage-collected before the worker thread fires.
    """
    result = pyqtSignal(LLMResult)
    error  = pyqtSignal(str)


class CouncilSignals(QObject):
    """Thread-safe Qt bridge for a council run.

    Signals
    -------
    member_started   (str)              — pass name about to be sent
    member_completed (str, LLMResult)   — pass returned successfully
    member_failed    (str, str)         — pass name, error message
    synthesis_started ()                — synthesis pass kicked off (Deliberate only)
    result           (CouncilResult)    — final consolidated result
    error            (str)              — fatal error (e.g. all passes failed)

    Storing CouncilSignals on `self` (not a local) is required so the
    underlying QObject lives long enough for the worker thread to fire.
    """
    member_started    = pyqtSignal(str)
    member_completed  = pyqtSignal(str, LLMResult)
    member_failed     = pyqtSignal(str, str)
    synthesis_started = pyqtSignal()
    result            = pyqtSignal(CouncilResult)
    error             = pyqtSignal(str)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LLMClient
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LLMClient:
    """Thin OpenAI-compatible /v1/chat/completions client for a llama.cpp server.

    The model is locked server-side; the `model` parameter is optional and
    only sent if explicitly set (some server configs require it, most ignore it).
    """

    def __init__(
        self,
        host:    str = LLAMA_DEFAULT_HOST,
        timeout: int = 120,
        # Legacy params — accepted but not required
        model:   str = "",
        api_key: str = "",
    ):
        self.host    = host.rstrip("/")
        self.timeout = timeout
        self.model   = model    # stored for display / legacy compat only
        self.api_key = api_key  # stored for legacy compat; not sent

    def complete(
        self,
        messages:    list[dict],
        max_tokens:  int   = 1024,
        temperature: float = 0.7,
        system:      str   = "",
    ) -> LLMResult:
        """Send a chat completion request and return an LLMResult.

        If `system` is provided it is prepended as a system message, replacing
        any existing system message at position 0.
        """
        msgs = list(messages)
        if system:
            # Prepend (or replace) the system message
            if msgs and msgs[0].get("role") == "system":
                msgs[0] = {"role": "system", "content": system}
            else:
                msgs.insert(0, {"role": "system", "content": system})

        url     = f"{self.host}/v1/chat/completions"
        payload: dict = {
            "messages":    msgs,
            "max_tokens":  max_tokens,
            "temperature": temperature,
            "stream":      False,
        }
        if self.model:
            payload["model"] = self.model

        body = json.dumps(payload).encode()
        req  = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        t0 = time.perf_counter()
        # Respect the global server-capacity semaphore. Callers from
        # different panels share the same pool so we don't overrun the
        # llama.cpp `--parallel` setting.
        with _REQUEST_SLOTS:
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode())
            except urllib.error.HTTPError as exc:
                raise RuntimeError(f"HTTP {exc.code}: {exc.reason}") from exc
            except urllib.error.URLError as exc:
                raise RuntimeError(f"Connection failed: {exc.reason}") from exc

        elapsed = int((time.perf_counter() - t0) * 1000)

        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("Empty response from llama.cpp server")

        content = ((choices[0].get("message") or {}).get("content") or "").strip()
        usage   = data.get("usage") or {}

        return LLMResult(
            text       = content,
            model      = data.get("model", ""),
            elapsed_ms = elapsed,
            tokens_in  = usage.get("prompt_tokens", 0),
            tokens_out = usage.get("completion_tokens", 0),
        )

    def complete_async(
        self,
        messages:    list[dict],
        max_tokens:  int   = 1024,
        temperature: float = 0.7,
        system:      str   = "",
        on_result:   "Callable[[LLMResult], None] | None" = None,
        on_error:    "Callable[[str], None] | None"       = None,
    ) -> None:
        """Fire-and-forget async wrapper around complete()."""
        def _worker():
            try:
                r = self.complete(messages, max_tokens, temperature, system)
                if on_result:
                    on_result(r)
            except Exception as exc:
                logger.warning("LLMClient async failed: %s", exc)
                if on_error:
                    on_error(str(exc))

        threading.Thread(target=_worker, daemon=True).start()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LightCouncil  (3 temperature passes + optional synthesis)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LightCouncil:
    """Three parallel passes at different temperatures.

    All calls hit the same llama.cpp server; the model is server-side locked.

    Passes
    ------
    Precise  (temp 0.2) — analytical, structured, accurate
    Balanced (temp 0.6) — well-rounded, thorough
    Creative (temp 1.0) — lateral, divergent, exploratory

    Modes
    -----
    Deliberate (default)
        After the 3 parallel passes complete, a synthesis pass (temp 0.4)
        sees all three responses and produces the final consolidated answer.
        Wall-clock ≈ slowest pass + synthesis pass.

    Quick
        After the 3 parallel passes complete, the longest non-empty response
        is returned as the final answer. No second LLM round-trip.
        Wall-clock ≈ slowest pass.
    """

    def __init__(
        self,
        host:         str = LLAMA_DEFAULT_HOST,
        timeout:      int = 120,
        default_mode: str = COUNCIL_DEFAULT_MODE,
        # Legacy params — accepted but silently ignored
        council_models:    "list[str] | None" = None,
        deliberator_model: str                = "",
        synthesis_mode:    str                = "",
        synthesis_model:   str                = "",
        tool_runner:       None               = None,
        role_overrides:    None               = None,
        api_key:           str                = "",
    ):
        self.host    = host.rstrip("/")
        self.timeout = timeout
        self._client = LLMClient(host=self.host, timeout=self.timeout)

        # Default mode used when complete() is called without an explicit mode
        self.default_mode = (
            default_mode if default_mode in COUNCIL_SYNTHESIS_MODES
            else COUNCIL_DEFAULT_MODE
        )

        # Legacy compat attributes used by some call sites
        self.council_models  = []
        self.synthesis_model = ""
        self.synthesis_mode  = synthesis_mode or self.default_mode
        self.api_key         = ""

    # ── Internal ──────────────────────────────────────────────────────────────

    def _run_pass(
        self,
        name:         str,
        temperature:  float,
        system:       str,
        messages:     list[dict],
        max_tokens:   int,
        on_started:   "Callable[[str], None] | None"           = None,
        on_completed: "Callable[[str, LLMResult], None] | None" = None,
        on_failed:    "Callable[[str, str], None] | None"      = None,
    ) -> tuple[str, "LLMResult | None", str]:
        """Run one council pass. Returns (name, result_or_None, error_str).

        Optional callbacks fire as the request enters/leaves the wire so that
        callers can stream progress to the UI without waiting for the slowest
        pass to finish.
        """
        if on_started:
            try: on_started(name)
            except Exception: logger.exception("Council on_started raised")
        try:
            r = self._client.complete(
                messages,
                max_tokens  = max_tokens,
                temperature = temperature,
                system      = system,
            )
            r.model = name
            if on_completed:
                try: on_completed(name, r)
                except Exception: logger.exception("Council on_completed raised")
            return name, r, ""
        except Exception as exc:
            err = str(exc)
            if on_failed:
                try: on_failed(name, err)
                except Exception: logger.exception("Council on_failed raised")
            return name, None, err

    def _run_parallel_passes(
        self,
        messages:     list[dict],
        max_tokens:   int,
        on_started:   "Callable[[str], None] | None"           = None,
        on_completed: "Callable[[str, LLMResult], None] | None" = None,
        on_failed:    "Callable[[str, str], None] | None"      = None,
    ) -> tuple[list[LLMResult], list[str]]:
        """Run all configured passes in parallel. Returns (members, failures).

        Each pass is throttled by the global server-capacity semaphore inside
        LLMClient.complete; the executor itself runs all passes immediately so
        that whichever pass enters the semaphore first starts work right away.
        """
        members: list[LLMResult] = []
        failed:  list[str]       = []

        with ThreadPoolExecutor(max_workers=len(COUNCIL_PASSES)) as pool:
            futures = {
                pool.submit(
                    self._run_pass, name, temp, system, messages, max_tokens,
                    on_started, on_completed, on_failed,
                ): name
                for name, temp, system in COUNCIL_PASSES
            }
            for fut in as_completed(futures):
                name, result, err = fut.result()
                if result:
                    members.append(result)
                else:
                    failed.append(f"{name}: {err}")
                    logger.warning("Council pass %s failed: %s", name, err)

        # Sort by defined pass order so callers see consistent ordering
        order = {name: i for i, (name, _, _) in enumerate(COUNCIL_PASSES)}
        members.sort(key=lambda r: order.get(r.model, 99))
        return members, failed

    # ── Public API ────────────────────────────────────────────────────────────

    def complete(
        self,
        messages:     list[dict],
        max_tokens:   int    = 1024,
        temperature:  float  = 0.6,   # ignored — each pass uses its own temperature
        mode:         "str | None" = None,
        on_member_started:   "Callable[[str], None] | None"           = None,
        on_member_completed: "Callable[[str, LLMResult], None] | None" = None,
        on_member_failed:    "Callable[[str, str], None] | None"      = None,
        on_synthesis_started: "Callable[[], None] | None"             = None,
    ) -> CouncilResult:
        """Run all passes in parallel, then either synthesise or pick longest.

        Parameters
        ----------
        mode
            Override the council's default mode for this call. One of
            COUNCIL_MODE_DELIBERATE or COUNCIL_MODE_QUICK. If None, uses
            self.default_mode.
        on_member_started / on_member_completed / on_member_failed
            Optional progress callbacks fired from worker threads as each
            council pass begins, completes, or errors out. Use these to
            stream cards into the UI as they arrive.
        on_synthesis_started
            Fired right before the (Deliberate-mode) synthesis pass is sent.
        """
        active_mode = mode or self.default_mode
        if active_mode not in COUNCIL_SYNTHESIS_MODES:
            active_mode = COUNCIL_DEFAULT_MODE

        members, failed = self._run_parallel_passes(
            messages, max_tokens,
            on_started   = on_member_started,
            on_completed = on_member_completed,
            on_failed    = on_member_failed,
        )

        if not members:
            raise RuntimeError(
                "All council passes failed:\n" + "\n".join(failed)
            )

        # ── QUICK mode: skip synthesis, pick longest non-empty ──────────────
        if active_mode == COUNCIL_MODE_QUICK:
            non_empty = [m for m in members if (m.text or "").strip()]
            picked    = max(non_empty, key=lambda r: len(r.text)) if non_empty else members[0]
            final     = LLMResult(
                text       = picked.text,
                model      = f"{picked.model} (quick)",
                elapsed_ms = picked.elapsed_ms,
                tokens_in  = sum(m.tokens_in  for m in members),
                tokens_out = sum(m.tokens_out for m in members),
            )
            return CouncilResult(members=members, final=final,
                                 failed=failed, mode=active_mode)

        # ── DELIBERATE mode: build synthesis prompt and run a 4th pass ──────
        synth_lines = [
            "You are a synthesiser. Below are responses from three reasoning passes "
            "with different styles. Combine their insights into a single, well-structured "
            "answer. Resolve any conflicts by favouring accuracy. Be concise and clear.\n"
        ]
        for r in members:
            synth_lines.append(f"### {r.model} pass\n{r.text}\n")
        synth_lines.append(
            "\nNow write the final consolidated answer in clear, well-structured prose."
        )

        if on_synthesis_started:
            try: on_synthesis_started()
            except Exception: logger.exception("Council on_synthesis_started raised")

        try:
            final = self._client.complete(
                messages,
                max_tokens  = max_tokens,
                temperature = SYNTHESIS_TEMPERATURE,
                system      = "\n".join(synth_lines),
            )
            final.model = "Synthesis"
        except Exception as exc:
            logger.warning("Synthesis pass failed, falling back to best member: %s", exc)
            best  = max(members, key=lambda r: len(r.text or ""))
            final = LLMResult(
                text       = best.text,
                model      = f"{best.model} (synthesis failed)",
                elapsed_ms = best.elapsed_ms,
            )

        return CouncilResult(members=members, final=final,
                             failed=failed, mode=active_mode)

    def complete_async(
        self,
        messages:             list[dict],
        max_tokens:           int   = 1024,
        temperature:          float = 0.6,
        mode:                 "str | None"                              = None,
        on_result:            "Callable[[CouncilResult], None] | None"  = None,
        on_error:             "Callable[[str], None] | None"            = None,
        on_member_started:    "Callable[[str], None] | None"            = None,
        on_member_completed:  "Callable[[str, LLMResult], None] | None" = None,
        on_member_failed:     "Callable[[str, str], None] | None"       = None,
        on_synthesis_started: "Callable[[], None] | None"               = None,
    ) -> None:
        """Fire-and-forget async wrapper around complete().

        Per-member callbacks fire from background threads as each pass
        starts / finishes, allowing the UI to render member cards as they
        arrive instead of after the slowest pass returns.
        """
        def _worker():
            try:
                r = self.complete(
                    messages, max_tokens, temperature, mode=mode,
                    on_member_started   = on_member_started,
                    on_member_completed = on_member_completed,
                    on_member_failed    = on_member_failed,
                    on_synthesis_started = on_synthesis_started,
                )
                if on_result:
                    on_result(r)
            except Exception as exc:
                logger.warning("LightCouncil async failed: %s", exc)
                if on_error:
                    on_error(str(exc))

        threading.Thread(target=_worker, daemon=True).start()


# Legacy alias — keeps any remaining LLMCouncil references working unchanged
LLMCouncil = LightCouncil


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Config helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def load_llm_client() -> "LLMClient | None":
    """Return a configured LLMClient pointed at the llama.cpp server."""
    from src.config import load_config
    cfg  = load_config()
    host = cfg.get("llama_host", LLAMA_DEFAULT_HOST).strip() or LLAMA_DEFAULT_HOST
    return LLMClient(host=host)


def save_llm_config(
    host:    str = LLAMA_DEFAULT_HOST,
    # Legacy params — silently ignored
    model:   str = "",
    api_key: str = "",
) -> None:
    """Persist llama.cpp host to config."""
    from src.config import load_config, save_config
    cfg = load_config()
    cfg["llama_host"] = host.strip() or LLAMA_DEFAULT_HOST
    save_config(cfg)


def load_council_config() -> "LightCouncil | None":
    """Return a configured LightCouncil, or None if council is disabled.

    Also re-applies the saved request concurrency to the global semaphore
    so changes from the Network → AI tab take effect on the next call.
    """
    from src.config import load_config
    cfg = load_config()
    set_request_concurrency(int(cfg.get("council_concurrency",
                                        COUNCIL_DEFAULT_CONCURRENCY)))
    if not cfg.get("council_enabled", False):
        return None
    host = cfg.get("llama_host", LLAMA_DEFAULT_HOST).strip() or LLAMA_DEFAULT_HOST
    mode = cfg.get("council_mode", COUNCIL_DEFAULT_MODE)
    return LightCouncil(host=host, default_mode=mode)


def save_council_config(
    enabled:    bool,
    mode:       str = COUNCIL_DEFAULT_MODE,
    concurrency: int = COUNCIL_DEFAULT_CONCURRENCY,
    # Legacy params — silently ignored
    models:          "list[str] | None" = None,
    synthesis_model: str                = "",
    synthesis_mode:  str                = "",
    tools_enabled:   bool               = False,
    role_overrides:  "dict | None"      = None,
) -> None:
    """Persist council enabled flag, mode, and concurrency to config."""
    from src.config import load_config, save_config
    cfg = load_config()
    cfg["council_enabled"]     = enabled
    cfg["council_mode"]        = mode if mode in COUNCIL_SYNTHESIS_MODES else COUNCIL_DEFAULT_MODE
    cfg["council_concurrency"] = max(1, min(int(concurrency), 16))
    save_config(cfg)
    set_request_concurrency(cfg["council_concurrency"])