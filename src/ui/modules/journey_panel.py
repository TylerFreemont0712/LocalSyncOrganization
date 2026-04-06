"""Journey Panel — goal-driven step tutoring with Council AI.

Fixed in this revision
──────────────────────
  • create_journey SQL bug (backtick in string) — fixed in journey_store.py
  • RoadmapFlowWidget snake arrow geometry bugs — replaced with simple horizontal
    single-row RoadmapWidget (no snake, no row reversal, scrollable)
  • Council synthesis not rendering — now shows member responses as fallback,
    plus a visible error state rather than silently empty
  • Auto-convene on journey/step creation removed — council is 100 % manual
  • Roadmap nodes are selectable: clicking one updates the step-detail panel
    and highlights the node with an accent ring
  • "Update Roadmap" in Workspace sends notes+hints to LLM and re-writes the roadmap
  • Off-roadmap steps are recorded as detours in roadmap_json

Tabs
────
  📋 Overview  : Roadmap flow → selected-step detail → council synthesis/checklist
  ⚔  Council   : All session comparison cards + quest log
  ✏  Workspace : Notes, hints, Convene Council, Complete Step, Update Roadmap

Dependencies: markdown (pip install markdown), stdlib urllib
"""

from __future__ import annotations

import json
import logging
import threading
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Optional

try:
    import markdown as _md_lib
    _HAS_MARKDOWN = True
except ImportError:
    _HAS_MARKDOWN = False

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QColor, QFont, QPainter, QPen, QBrush, QPainterPath,
)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QTextBrowser, QScrollArea, QFrame, QSplitter,
    QDialog, QLineEdit, QCheckBox, QStackedWidget, QTabWidget,
    QToolButton, QMessageBox, QMenu, QComboBox, QSizePolicy,
)

from src.data.journey_store import (
    JourneyStore, Journey, JourneyStep, CouncilSession,
    Roadmap, RoadmapStep,
    JOURNEY_DOMAINS, DOMAIN_COLORS,
)
from src.utils.llm import (
    LLMClient, LLMCouncil, CouncilResult,
    load_llm_client, load_council_config,
)

logger = logging.getLogger(__name__)

_FALLBACK = {
    "bg": "#1e1e2e", "surface": "#313244", "border": "#45475a",
    "fg": "#cdd6f4", "muted": "#7f849c", "hover": "#3b3d54",
    "accent": "#89b4fa", "accent_fg": "#1e1e2e",
    "accent_hover": "#a0c5ff", "accent_pressed": "#74a4ea",
    "red": "#f38ba8", "red_hover": "#f5a0b8",
    "green": "#a6e3a1", "yellow": "#f9e2af",
    "header_bg": "#181825", "alt_row": "#252538",
}

_TAB_OVERVIEW  = 0
_TAB_COUNCIL   = 1
_TAB_WORKSPACE = 2

# ── Journey templates ─────────────────────────────────────────────────────────

JOURNEY_TEMPLATES: dict[str, dict | None] = {
    "── Coding ──": None,
    "Learn Python (Beginner → Intermediate)": {
        "domain": "Coding",
        "goal": (
            "Build solid Python foundations progressing from environment setup through "
            "core language features (data types, control flow, functions, OOP) to practical "
            "skills including file I/O, error handling, and a capstone project."
        ),
        "steps": [
            "Environment Setup & Hello World",
            "Variables, Types & Basic I/O",
            "Control Flow: Conditionals & Loops",
            "Functions, Scope & Recursion",
            "Lists, Dicts, Tuples & Sets",
            "File I/O & Exception Handling",
            "Object-Oriented Programming Fundamentals",
            "Modules, Packages & the Standard Library",
            "Capstone Project",
        ],
    },
    "Learn JavaScript & Modern Web Dev": {
        "domain": "Coding",
        "goal": (
            "Master JavaScript from fundamentals through modern ES6+ features, DOM "
            "manipulation, async programming, and the Fetch API."
        ),
        "steps": [
            "Setup, Browser DevTools & Hello JS",
            "Variables, Types & Operators",
            "Functions, Scope & Closures",
            "Arrays, Objects & Destructuring",
            "DOM Manipulation & Events",
            "Promises & Async/Await",
            "Fetch API & Working with REST",
            "ES6+ Features & Modern Patterns",
            "Mini Project: Interactive Web App",
        ],
    },
    "Build a REST API": {
        "domain": "Coding",
        "goal": (
            "Design and implement a production-ready REST API with routing, "
            "database integration, authentication, validation, testing, and deployment."
        ),
        "steps": [
            "API Design & OpenAPI Specification",
            "Project Setup, Framework & Routing",
            "Database Schema & ORM Integration",
            "CRUD Endpoints Implementation",
            "Authentication & JWT / Session Management",
            "Input Validation & Error Handling",
            "Unit & Integration Testing",
            "Documentation & Deployment",
        ],
    },
    "── Language Learning ──": None,
    "Learn Japanese (N5 → N4)": {
        "domain": "Language Learning",
        "goal": (
            "Achieve solid N5 and introductory N4 Japanese: master hiragana, katakana, "
            "core N5 kanji and grammar, reach 500+ vocabulary, and hold basic conversations."
        ),
        "steps": [
            "Hiragana: Full Mastery",
            "Katakana: Full Mastery",
            "Greetings, Self-Introduction & Basic Phrases",
            "Numbers, Time & Dates",
            "Core N5 Grammar",
            "Essential Vocabulary (500 words, SRS)",
            "N5 Kanji (80 characters)",
            "Simple Dialogues & Listening Practice",
            "N4 Grammar Introduction",
        ],
    },
    "── Business / Freelance ──": None,
    "Build a Freelance Business from Zero": {
        "domain": "Business / Freelance",
        "goal": (
            "Go from zero to first paying client: define your niche, build a portfolio, "
            "price your services confidently, set up outreach, and win contracts."
        ),
        "steps": [
            "Niche Definition & Skill Audit",
            "Ideal Client Research",
            "Portfolio: 3 Sample Projects",
            "Pricing Strategy & Service Packages",
            "Platform Setup & Profile Optimisation",
            "First Outreach Campaign (20 contacts)",
            "Proposal & Contract Templates",
            "Client Onboarding & Delivery System",
        ],
    },
    "── Health & Fitness ──": None,
    "Beginner Strength Training (12 Weeks)": {
        "domain": "Health & Fitness",
        "goal": (
            "Build a sustainable strength training foundation in 12 weeks: master the 5 "
            "compound movements, establish progressive overload habits, and see gains."
        ),
        "steps": [
            "Baseline Assessment & Goal Setting",
            "The Big 5 Movements — Form & Safety",
            "Weeks 1-2: Foundation Program",
            "Nutrition Basics & Protein Targets",
            "Progressive Overload Principles",
            "Weeks 3-6: Building Phase",
            "Recovery, Sleep & Deload Strategy",
            "Weeks 7-12: Strength Phase",
            "Progress Assessment & Next Cycle",
        ],
    },
}

# ── Tutor system prompt ───────────────────────────────────────────────────────

_TUTOR_SYSTEM = (
    "You are an expert tutor, mentor, and educator providing a detailed, "
    "lesson-plan style tutoring session. Your advice must be thorough — not a brief summary.\n\n"
    "For every step you advise on, include:\n"
    "1. Clear explanation of the core concepts\n"
    "2. Step-by-step instructions the learner can follow right now\n"
    "3. Concrete examples, code snippets, exercises, or practice tasks\n"
    "4. Common mistakes and misconceptions to avoid\n"
    "5. How to know the step is genuinely complete (success criteria)\n"
    "6. A rough time estimate\n\n"
    "Be generous with depth. This is a tutoring session, not a quick answer. "
    "Respond using markdown — headers (##), bold, bullet lists, and code blocks."
)

# ── Web search ────────────────────────────────────────────────────────────────

def _ddg_search(query: str, timeout: int = 8) -> str:
    url = ("https://api.duckduckgo.com/?q="
           + urllib.parse.quote_plus(query)
           + "&format=json&no_html=1&skip_disambig=1")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LocalSync/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        parts: list[str] = []
        abstract = data.get("AbstractText", "").strip()
        if abstract:
            parts.append(abstract[:400])
        for topic in data.get("RelatedTopics", [])[:3]:
            txt = topic.get("Text", "").strip() if isinstance(topic, dict) else ""
            if txt:
                parts.append(txt[:200])
        return "\n".join(parts) if parts else ""
    except Exception as exc:
        logger.debug("DDG search failed for %r: %s", query, exc)
        return ""


def _generate_search_queries(client: LLMClient, journey_title: str,
                              step_title: str, domain: str) -> list[str]:
    prompt = (
        f"Journey: {journey_title}\nStep: {step_title}\nDomain: {domain}\n\n"
        "List exactly 2 concise web search queries (one per line, no numbering) "
        "for the most useful current information to tutor this step."
    )
    try:
        r = client.complete([{"role": "user", "content": prompt}],
                            max_tokens=80, temperature=0.3)
        return [ln.strip().lstrip("-\u2022*").strip()
                for ln in r.text.strip().splitlines() if ln.strip()][:3]
    except Exception:
        return []


# ── Context builder ───────────────────────────────────────────────────────────

def _build_context(
    journey: Journey, steps: list[JourneyStep], current_step: JourneyStep,
    web_snippets: dict, todo_store=None, activity_store=None, calendar_store=None,
) -> str:
    roadmap = journey.roadmap
    L: list[str] = [
        "=" * 44, "  JOURNEY CONTEXT", "=" * 44, "",
        f"Journey : {journey.title}",
        f"Domain  : {journey.domain}",
        f"Goal    : {journey.goal_description}", "",
    ]
    if roadmap.steps:
        L.append("-- Planned Roadmap --")
        if roadmap.overview:
            L.append(f"  {roadmap.overview}")
        for rs in roadmap.steps:
            status = "done" if any(
                s.title.strip().lower() == rs.title.strip().lower()
                and s.status == "completed" for s in steps) else ""
            marker = "\u2713" if status == "done" else (
                ">" if rs.title.strip().lower() == current_step.title.strip().lower()
                else " ")
            detour = " [DETOUR]" if rs.is_detour else ""
            L.append(f"  [{marker}] Step {rs.number}: {rs.title}{detour}")
        L.append("")
    done = [s for s in steps if s.status == "completed"]
    if done:
        L.append("-- Completed Steps --")
        for s in done:
            L.append(f"  \u2713 Step {s.step_number}: {s.title}")
            if s.user_notes:
                L.append(f"    Notes: {s.user_notes[:200]}")
        L.append("")
    L += [
        "-- CURRENT STEP (provide thorough tutoring) --",
        f"  Step {current_step.step_number}: {current_step.title}",
    ]
    if current_step.user_notes:
        L.append(f"  Learner notes: {current_step.user_notes[:500]}")
    if current_step.user_next_suggestions:
        L.append(f"  Hints: {current_step.user_next_suggestions[:400]}")
    L.append("")
    try:
        if todo_store:
            todos = [t for t in todo_store.get_all(include_done=False)][:8]
            if todos:
                L.append("-- Open Tasks --")
                for t in todos:
                    due = f" due {t.due_date}" if getattr(t, "due_date", None) else ""
                    L.append(f"  \u2022 {t.title}{due}")
                L.append("")
    except Exception:
        pass
    try:
        if calendar_store:
            now_ts = datetime.now(timezone.utc)
            events = calendar_store.get_events(
                start=now_ts.isoformat(),
                end=(now_ts + timedelta(days=7)).isoformat())[:6]
            if events:
                L.append("-- Upcoming Calendar --")
                for ev in events:
                    L.append(f"  \u2022 {ev.title} [{ev.start_time[:10]}]")
                L.append("")
    except Exception:
        pass
    try:
        if activity_store:
            week_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
            acts = [a for a in activity_store.get_all() if a.date >= week_ago]
            if acts:
                totals: dict[str, float] = {}
                for a in acts:
                    try:
                        s2 = datetime.strptime(a.start_time, "%H:%M")
                        e2 = datetime.strptime(a.end_time,   "%H:%M")
                        totals[a.activity] = totals.get(a.activity, 0) + (e2-s2).seconds/3600
                    except Exception:
                        pass
                L.append("-- Activity This Week --")
                for act, hrs in sorted(totals.items(), key=lambda x: -x[1])[:5]:
                    L.append(f"  \u2022 {act}: {hrs:.1f}h")
                L.append("")
    except Exception:
        pass
    if web_snippets:
        L.append("-- Web Search --")
        for q, snip in web_snippets.items():
            if snip:
                L += [f'  "{q}"', f"  {snip[:400]}", ""]
    L += ["=" * 44, "  END OF CONTEXT", "=" * 44]
    return "\n".join(L)


# ── Structured content parser ─────────────────────────────────────────────────

def _parse_structured(text: str) -> tuple[list[str], list[str], str]:
    checklist: list[str] = []
    resources: list[str] = []
    roadmap_lines: list[str] = []
    section = None
    for line in text.splitlines():
        s = line.strip()
        u = s.upper().rstrip(":")
        if u in ("CHECKLIST", "TASKS", "ACTION ITEMS", "TO DO", "TODO"):
            section = "c"; continue
        if u in ("RESOURCES", "REFERENCES", "TOOLS", "FURTHER READING"):
            section = "r"; continue
        if u in ("ROADMAP", "NEXT STEPS", "WHAT COMES NEXT", "COMING UP"):
            section = "m"; continue
        if not s:
            continue
        task = s.lstrip("-\u2022*0123456789.) ").strip()
        if not task:
            continue
        if section == "c":
            checklist.append(task)
        elif section == "r":
            resources.append(task)
        elif section == "m":
            roadmap_lines.append(s)
    return checklist[:10], resources[:8], " ".join(roadmap_lines).strip()


def _run_structured_call(
    client: LLMClient, synthesis: str,
    journey: Journey, step: JourneyStep,
) -> tuple[list[str], list[str], str]:
    prompt = (
        f'Structured action plan for Step {step.step_number}: "{step.title}"\n'
        f'Journey: "{journey.title}" ({journey.domain})\n\n'
        f"Council synthesis:\n{synthesis[:1600]}\n\n"
        "Produce exactly THREE sections. Use these EXACT headers on their own lines:\n\n"
        "CHECKLIST:\n"
        "(6-10 concrete actionable tasks. One per line starting with '- ')\n\n"
        "RESOURCES:\n"
        "(4-6 specific resources: docs, books, tools. One per line starting with '- ')\n\n"
        "ROADMAP:\n"
        "(3-5 sentences: what comes after this step, previewing the next 2-3 steps)\n\n"
        "Return ONLY these three sections."
    )
    try:
        r = client.complete([{"role": "user", "content": prompt}],
                            max_tokens=800, temperature=0.3)
        return _parse_structured(r.text)
    except Exception as exc:
        logger.debug("Structured call failed: %s", exc)
        return [], [], ""


# ── Roadmap generation ────────────────────────────────────────────────────────

def _generate_roadmap(client: LLMClient, journey: Journey) -> Roadmap:
    prompt = (
        f'Design a complete learning roadmap:\n\n'
        f'Title  : {journey.title}\n'
        f'Domain : {journey.domain}\n'
        f'Goal   : {journey.goal_description}\n\n'
        "Create 6-10 steps that logically progress from foundations to mastery.\n\n"
        "Return VALID JSON only (no markdown fences, no extra text):\n"
        '{\n'
        '  "overview": "2-3 sentence description of the full learning path",\n'
        '  "steps": [\n'
        '    {\n'
        '      "number": 1,\n'
        '      "title": "Action-oriented step title (5-8 words)",\n'
        '      "description": "1-2 sentences on what this step covers and why",\n'
        '      "objectives": ["Objective 1", "Objective 2"]\n'
        '    }\n'
        '  ]\n'
        '}\n'
    )
    try:
        r    = client.complete([{"role": "user", "content": prompt}],
                               max_tokens=1400, temperature=0.4)
        text = r.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.lower().startswith("json"):
                text = text[4:]
            text = text.strip()
        data  = json.loads(text)
        steps = [
            RoadmapStep(
                number=s.get("number", i + 1),
                title=s.get("title", f"Step {i+1}"),
                description=s.get("description", ""),
                objectives=s.get("objectives", []),
            )
            for i, s in enumerate(data.get("steps", []))
        ]
        return Roadmap(overview=data.get("overview", ""), steps=steps)
    except Exception as exc:
        logger.warning("Roadmap generation failed: %s", exc)
        return Roadmap(overview="")


def _update_roadmap_from_pivot(
    client: LLMClient, journey: Journey, steps: list[JourneyStep],
    pivot_request: str,
) -> Roadmap:
    """Re-generate the roadmap based on a pivot request from the workspace."""
    current_roadmap = journey.roadmap
    done_titles = [s.title for s in steps if s.status == "completed"]
    prompt = (
        f'Update this learning roadmap based on a pivot request.\n\n'
        f'Journey: {journey.title}\n'
        f'Goal   : {journey.goal_description}\n\n'
        f'Completed steps (do NOT remove these):\n'
        + "\n".join(f"  - {t}" for t in done_titles) + "\n\n"
        f'Pivot request from learner:\n{pivot_request}\n\n'
        f'Current roadmap overview:\n{current_roadmap.overview}\n\n'
        "Rewrite the roadmap to incorporate the pivot. "
        "Keep completed steps unchanged. Adjust or add future steps as needed.\n"
        "Mark any newly added detour steps with \"is_detour\": true.\n\n"
        "Return VALID JSON only:\n"
        '{\n'
        '  "overview": "Updated overview reflecting the pivot",\n'
        '  "steps": [\n'
        '    {\n'
        '      "number": 1,\n'
        '      "title": "...",\n'
        '      "description": "...",\n'
        '      "objectives": [...],\n'
        '      "is_detour": false\n'
        '    }\n'
        '  ]\n'
        '}\n'
    )
    try:
        r    = client.complete([{"role": "user", "content": prompt}],
                               max_tokens=1400, temperature=0.4)
        text = r.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.lower().startswith("json"):
                text = text[4:]
            text = text.strip()
        data  = json.loads(text)
        steps_out = [
            RoadmapStep(
                number=s.get("number", i + 1),
                title=s.get("title", f"Step {i+1}"),
                description=s.get("description", ""),
                objectives=s.get("objectives", []),
                is_detour=bool(s.get("is_detour", False)),
                branch_from=s.get("branch_from"),
            )
            for i, s in enumerate(data.get("steps", []))
        ]
        return Roadmap(overview=data.get("overview", ""), steps=steps_out)
    except Exception as exc:
        logger.warning("Roadmap pivot failed: %s", exc)
        return current_roadmap


# ── Council pipeline (uses existing LLMCouncil) ───────────────────────────────

def _run_council(
    journey: Journey, steps: list[JourneyStep], current_step: JourneyStep,
    llm_client: LLMClient, council: LLMCouncil, journey_store: JourneyStore,
    todo_store=None, activity_store=None, calendar_store=None, on_progress=None,
) -> CouncilSession:
    def _prog(msg: str):
        if on_progress:
            on_progress(msg)

    # Optional web search
    web_snippets: dict[str, str] = {}
    web_queries:  list[str]      = []
    if journey.web_search_enabled:
        _prog("\U0001f310 Generating search queries\u2026")
        web_queries = _generate_search_queries(
            llm_client, journey.title, current_step.title, journey.domain)
        if web_queries:
            _prog(f"\U0001f50d Searching\u2026")
            for q in web_queries:
                snip = _ddg_search(q)
                if snip:
                    web_snippets[q] = snip

    _prog("\U0001f4cb Assembling context\u2026")
    context = _build_context(journey, steps, current_step, web_snippets,
                             todo_store, activity_store, calendar_store)

    user_q = (
        f"Provide a comprehensive tutoring session for Step {current_step.step_number}: "
        f'"{current_step.title}".\n\n'
        "Be thorough and educational — include concepts, examples, exercises, "
        "common mistakes, and success criteria. Aim for a full lesson-plan response. "
        "Use markdown formatting."
    )

    messages = [
        {"role": "system", "content": _TUTOR_SYSTEM + "\n\n" + context},
        {"role": "user",   "content": user_q},
    ]

    # Fan-out via LLMCouncil
    _prog(f"\u2694  Convening council ({len(council.council_models)} models)\u2026")
    synthesis_text  = ""
    synthesis_model = council.synthesis_model or (council.council_models[0] if council.council_models else "")
    member_records:  list[dict] = []

    try:
        result: CouncilResult = council.complete(
            messages, max_tokens=1400, temperature=0.6)

        # Extract synthesis
        synthesis_text  = (result.final.text or "").strip()
        synthesis_model = result.final.model or synthesis_model

        # Build member records
        for r in result.members:
            member_records.append({
                "label":    r.model.split("/")[-1].replace(":free","").replace(":nitro",""),
                "model":    r.model,
                "response": r.text or "",
                "ok":       True,
            })
        for failed_model in result.failed_models:
            member_records.append({
                "label":    failed_model.split("/")[-1],
                "model":    failed_model,
                "response": "[Model did not respond]",
                "ok":       False,
            })

        _prog(f"  \u2713 {result.member_count} model(s) responded")

        # If synthesis is empty, compose from individual members as fallback
        if not synthesis_text and result.members:
            parts = []
            for r in result.members:
                if r.text and r.text.strip():
                    short_name = r.model.split("/")[-1].replace(":free","").replace(":nitro","")
                    parts.append(f"## {short_name}\n\n{r.text.strip()}")
            if parts:
                synthesis_text = "\n\n---\n\n".join(parts)
                synthesis_text = (
                    "_Note: Synthesis model returned empty — showing individual model "
                    "responses below._\n\n" + synthesis_text
                )

    except Exception as exc:
        logger.warning("council.complete() failed: %s", exc)
        # Fallback: try a single direct call
        _prog(f"  \u26a0 Council error, trying single model\u2026")
        try:
            r = llm_client.complete(messages, max_tokens=1400, temperature=0.6)
            synthesis_text  = r.text or ""
            synthesis_model = r.model or synthesis_model
            member_records.append({
                "label":    synthesis_model.split("/")[-1],
                "model":    synthesis_model,
                "response": synthesis_text,
                "ok":       True,
            })
        except Exception as exc2:
            synthesis_text = (
                f"## Council Unavailable\n\n"
                f"All models failed to respond.\n\n"
                f"Council error: {exc}\n\nFallback error: {exc2}"
            )

    if not synthesis_text:
        synthesis_text = (
            "## No Response\n\n"
            "The council returned an empty response. "
            "This can happen with certain free models — try convening again, "
            "or check your council model configuration."
        )

    # Structured content call
    _prog("\U0001f4cb Building action plan\u2026")
    struct_client = LLMClient(api_key=council.api_key,
                               model=synthesis_model or council.council_models[0],
                               timeout=council.timeout)
    checklist, resources, roadmap_text = _run_structured_call(
        struct_client, synthesis_text, journey, current_step)

    _prog("\U0001f4be Saving\u2026")
    session = journey_store.save_council_session(
        step_id=current_step.id, synthesis=synthesis_text,
        synthesis_model=synthesis_model, synthesis_mode=council.synthesis_mode,
        web_search_used=bool(web_snippets), web_search_queries=web_queries,
        member_records=member_records,
        step_checklist=checklist, step_resources=resources, roadmap_text=roadmap_text,
    )
    _prog("\u2705 Complete")
    return session


# ── HTML renderer ─────────────────────────────────────────────────────────────

def _to_html(text: str, p: dict) -> str:
    bg     = p.get("bg",      "#1e1e2e")
    fg     = p.get("fg",      "#cdd6f4")
    muted  = p.get("muted",   "#7f849c")
    accent = p.get("accent",  "#89b4fa")
    green  = p.get("green",   "#a6e3a1")
    border = p.get("border",  "#45475a")
    if _HAS_MARKDOWN:
        body = _md_lib.markdown(text, extensions=["nl2br", "fenced_code", "tables"])
    else:
        import html as _h
        body = "<p>" + _h.escape(text).replace("\n\n", "</p><p>") + "</p>"
    return (
        "<html><head><style>"
        f"body{{background:{bg};color:{fg};font-family:'Segoe UI','Meiryo UI',sans-serif;"
        f"font-size:13px;line-height:1.75;margin:16px;}}"
        f"h1,h2{{color:{accent};border-bottom:1px solid {border};"
        f"padding-bottom:5px;margin-top:20px;}}"
        f"h3{{color:{accent};margin-top:14px;}}"
        f"code{{background:{border};color:{green};padding:2px 6px;"
        f"border-radius:4px;font-family:'Consolas','Courier New',monospace;font-size:12px;}}"
        f"pre{{background:{border};padding:14px;border-radius:8px;overflow-x:auto;margin:10px 0;}}"
        f"pre code{{background:transparent;padding:0;}}"
        f"blockquote{{border-left:3px solid {accent};margin-left:0;padding-left:14px;color:{muted};}}"
        f"a{{color:{accent};}}"
        f"li{{margin:5px 0;}}ul,ol{{padding-left:20px;}}"
        f"strong{{color:{accent};}}em{{color:{muted};font-style:italic;}}"
        f"table{{border-collapse:collapse;width:100%;margin:10px 0;}}"
        f"th,td{{border:1px solid {border};padding:8px 12px;}}"
        f"th{{background:{border};color:{accent};}}"
        f"p{{margin:8px 0;}}hr{{border:none;border-top:1px solid {border};margin:14px 0;}}"
        "</style></head>"
        f"<body>{body}</body></html>"
    )


def _tab_style(p: dict) -> str:
    bg=p.get("bg","#1e1e2e"); surface=p.get("surface","#313244")
    border=p.get("border","#45475a"); fg=p.get("fg","#cdd6f4")
    muted=p.get("muted","#7f849c"); accent=p.get("accent","#89b4fa")
    hover=p.get("hover","#3b3d54")
    return (
        f"QTabWidget::pane{{background:{bg};border:1px solid {border};"
        f"border-top:none;border-radius:0 0 10px 10px;}}"
        f"QTabBar::tab{{background:{surface};color:{muted};"
        f"border:1px solid {border};border-bottom:none;"
        f"padding:10px 24px;font-size:11px;font-weight:bold;letter-spacing:1px;"
        f"border-radius:6px 6px 0 0;margin-right:3px;min-width:90px;}}"
        f"QTabBar::tab:selected{{background:{bg};color:{accent};"
        f"border-bottom:2px solid {accent};}}"
        f"QTabBar::tab:hover:!selected{{background:{hover};color:{fg};}}"
        f"QTabWidget QScrollArea{{background:transparent;border:none;}}"
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  Custom widgets
# ═══════════════════════════════════════════════════════════════════════════════

class RoadmapWidget(QWidget):
    """
    Horizontal roadmap flow — simple single row, scrollable.
    No snake / no row reversal — eliminates all previous arrow geometry bugs.
    Each node is a rounded rect with a step-number badge, title, and status.
    Clicking a node selects it (accent ring) and emits node_selected(index).
    """
    node_selected = pyqtSignal(int)   # 0-based index into roadmap.steps

    _NW     = 158   # node width
    _NH     = 62    # node height
    _GAP    = 28    # gap between nodes (the arrow lives here)
    _PAD_X  = 10
    _PAD_Y  = 8
    _LABEL_H = 16   # height for status text below nodes
    _R      = 8     # corner radius
    _BR     = 10    # badge radius

    def __init__(self, parent=None):
        super().__init__(parent)
        self._roadmap:      Roadmap           = Roadmap(overview="")
        self._steps:        list[JourneyStep] = []
        self._palette:      dict              = dict(_FALLBACK)
        self._selected_idx: int               = -1
        self._hovered_idx:  int               = -1
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_size()

    def set_palette(self, p: dict):
        self._palette = p; self.update()

    def set_data(self, roadmap: Roadmap, steps: list[JourneyStep],
                 selected_idx: int = -1):
        self._roadmap      = roadmap
        self._steps        = steps
        self._selected_idx = selected_idx
        self._update_size(); self.update()

    def set_selected(self, idx: int):
        self._selected_idx = idx; self.update()

    def _update_size(self):
        n = len(self._roadmap.steps)
        w = self._PAD_X*2 + n*self._NW + max(n-1, 0)*self._GAP if n else 100
        h = self._PAD_Y*2 + self._NH + self._LABEL_H
        self.setMinimumSize(w, h)
        self.setFixedHeight(h)

    def _node_x(self, i: int) -> int:
        return self._PAD_X + i * (self._NW + self._GAP)

    def _step_status(self, rs: RoadmapStep) -> str:
        title_l = rs.title.strip().lower()
        for s in self._steps:
            if s.title.strip().lower() == title_l:
                return s.status
        return "unstarted"

    def paintEvent(self, _):
        n = len(self._roadmap.steps)
        if n == 0:
            return
        p  = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        ny = self._PAD_Y

        accent  = QColor(self._palette.get("accent",  "#89b4fa"))
        green   = QColor(self._palette.get("green",   "#a6e3a1"))
        surface = QColor(self._palette.get("surface", "#313244"))
        border  = QColor(self._palette.get("border",  "#45475a"))
        fg      = QColor(self._palette.get("fg",      "#cdd6f4"))
        muted   = QColor(self._palette.get("muted",   "#7f849c"))
        acc_fg  = QColor(self._palette.get("accent_fg","#1e1e2e"))
        yellow  = QColor(self._palette.get("yellow",  "#f9e2af"))

        for i, rs in enumerate(self._roadmap.steps):
            nx       = self._node_x(i)
            nw, nh   = self._NW, self._NH
            cy       = ny + nh // 2
            status   = self._step_status(rs)
            selected = (i == self._selected_idx)
            hov      = (i == self._hovered_idx)
            detour   = rs.is_detour

            # Colors
            if status == "completed":
                fill, text_c, bord_c = green, QColor("#1e1e2e"), green.darker(130)
            elif status == "active":
                fill = accent.lighter(108) if hov else accent
                text_c = acc_fg
                bord_c = accent.lighter(160)
            else:
                fill   = surface.lighter(108) if hov else surface
                text_c = fg if hov else muted
                bord_c = (yellow if detour else
                          (accent if selected else
                           (border.lighter(130) if hov else border)))

            # Selection ring (drawn before node body)
            if selected:
                sel = QColor(accent); sel.setAlpha(55)
                p.setBrush(QBrush(sel)); p.setPen(Qt.PenStyle.NoPen)
                p.drawRoundedRect(nx-5, ny-5, nw+10, nh+10, self._R+3, self._R+3)

            # Active glow
            if status == "active":
                glow = QColor(accent); glow.setAlpha(28)
                p.setBrush(QBrush(glow)); p.setPen(Qt.PenStyle.NoPen)
                p.drawRoundedRect(nx-4, ny-4, nw+8, nh+8, self._R+2, self._R+2)

            # Node body
            p.setBrush(QBrush(fill))
            p.setPen(QPen(bord_c, 1.8 if selected else 1.2))
            p.drawRoundedRect(nx, ny, nw, nh, self._R, self._R)

            # Detour stripe (top-left triangle in yellow)
            if detour:
                tri = QPainterPath()
                tri.moveTo(nx, ny)
                tri.lineTo(nx + 18, ny)
                tri.lineTo(nx, ny + 18)
                tri.closeSubpath()
                p.fillPath(tri, QBrush(yellow))

            # Badge circle with step number
            br = self._BR
            bx = nx + 14 + br
            p.setBrush(QBrush(bord_c)); p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(bx - br, cy - br, br*2, br*2)

            if status == "completed":
                # Checkmark inside badge
                p.setPen(QPen(QColor("#1e1e2e"), 1.8, Qt.PenStyle.SolidLine,
                              Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
                p.drawLine(bx - 4, cy,     bx - 1, cy + 3)
                p.drawLine(bx - 1, cy + 3, bx + 4, cy - 3)
            else:
                # Step number
                p.setPen(QPen(QColor("#ffffff") if status != "unstarted" else muted))
                p.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
                p.drawText(bx - br, cy - br, br*2, br*2,
                           Qt.AlignmentFlag.AlignCenter, str(rs.number))

            # Title text
            tx = bx + br + 6
            tw = nw - (tx - nx) - 6
            p.setPen(QPen(text_c))
            p.setFont(QFont("Segoe UI", 9,
                            QFont.Weight.Bold if status in ("active","completed")
                            else QFont.Weight.Normal))
            fm    = p.fontMetrics()
            title = rs.title
            if fm.horizontalAdvance(title) > tw:
                while title and fm.horizontalAdvance(title + "\u2026") > tw:
                    title = title[:-1]
                title += "\u2026"
            p.drawText(tx, ny, tw, nh,
                       Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                       title)

            # Status label below node
            status_txt = {
                "completed": "Done",
                "active":    "In Progress",
                "unstarted": "Upcoming",
            }.get(status, "")
            if detour and status == "unstarted":
                status_txt = "Detour"
            status_col = (green.darker(120) if status == "completed" else
                          (accent if status == "active" else
                           (yellow.darker(130) if detour else muted)))
            p.setPen(QPen(status_col))
            p.setFont(QFont("Segoe UI", 7))
            p.drawText(nx, ny + nh + 2, nw, self._LABEL_H,
                       Qt.AlignmentFlag.AlignHCenter, status_txt)

            # Arrow to next node — simple horizontal line + arrowhead
            if i < n - 1:
                ax_start = nx + nw + 2
                ax_end   = ax_start + self._GAP - 4
                ay       = cy
                p.setPen(QPen(border, 1.5))
                p.drawLine(ax_start, ay, ax_end - 6, ay)
                # Filled arrowhead triangle
                tri2 = QPainterPath()
                tri2.moveTo(ax_end,     ay)
                tri2.lineTo(ax_end - 7, ay - 4)
                tri2.lineTo(ax_end - 7, ay + 4)
                tri2.closeSubpath()
                p.fillPath(tri2, QBrush(border))
        p.end()

    def mouseMoveEvent(self, event):
        x, y  = event.position().x(), event.position().y()
        old   = self._hovered_idx
        self._hovered_idx = -1
        ny = self._PAD_Y
        for i, rs in enumerate(self._roadmap.steps):
            nx = self._node_x(i)
            if nx <= x <= nx + self._NW and ny <= y <= ny + self._NH:
                self._hovered_idx = i
                tip = f"Step {rs.number}: {rs.title}"
                if rs.description:
                    tip += f"\n{rs.description}"
                if rs.objectives:
                    tip += "\n\nObjectives:\n" + "\n".join(
                        f"  \u2022 {o}" for o in rs.objectives)
                if rs.is_detour:
                    tip += "\n\n[Detour step]"
                self.setToolTip(tip)
                break
        if self._hovered_idx != old:
            self.update()
        if self._hovered_idx < 0:
            self.setToolTip("")

    def leaveEvent(self, _):
        self._hovered_idx = -1; self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        x, y = event.position().x(), event.position().y()
        ny   = self._PAD_Y
        for i in range(len(self._roadmap.steps)):
            nx = self._node_x(i)
            if nx <= x <= nx + self._NW and ny <= y <= ny + self._NH:
                self._selected_idx = i
                self.update()
                self.node_selected.emit(i)
                return


class StepTrack(QWidget):
    step_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._steps:       list[JourneyStep] = []
        self._palette:     dict              = dict(_FALLBACK)
        self._hovered_idx: int               = -1
        self.setFixedHeight(82); self.setMinimumWidth(200)
        self.setMouseTracking(True)

    def set_palette(self, p: dict): self._palette = p; self.update()
    def set_steps(self, steps: list[JourneyStep]): self._steps = steps; self.update()

    def _node_cx(self, i: int) -> int:
        n = len(self._steps); margin = 28
        spacing = (self.width() - 2 * margin) / max(n - 1, 1) if n > 1 else 0
        return int(margin + spacing * i)

    def paintEvent(self, _):
        if not self._steps: return
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        n = len(self._steps); cy = 38; r = 13
        accent  = QColor(self._palette.get("accent",  "#89b4fa"))
        muted   = QColor(self._palette.get("muted",   "#7f849c"))
        green   = QColor(self._palette.get("green",   "#a6e3a1"))
        surface = QColor(self._palette.get("surface", "#313244"))
        border  = QColor(self._palette.get("border",  "#45475a"))
        if n > 1:
            p.setPen(QPen(border, 2))
            p.drawLine(self._node_cx(0), cy, self._node_cx(n - 1), cy)
        for i, step in enumerate(self._steps):
            cx = self._node_cx(i)
            done = step.status == "completed"; active = step.status == "active"
            hov  = (i == self._hovered_idx)
            if done:
                col = green.lighter(115) if hov else green
                p.setBrush(QBrush(col)); p.setPen(QPen(col.darker(120), 1))
                p.drawEllipse(cx-r, cy-r, r*2, r*2)
                p.setPen(QPen(QColor("#1e1e2e"), 2, Qt.PenStyle.SolidLine,
                              Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
                p.drawLine(cx-5, cy, cx-1, cy+4); p.drawLine(cx-1, cy+4, cx+5, cy-4)
            elif active:
                glow = QColor(accent); glow.setAlpha(40)
                p.setBrush(QBrush(glow)); p.setPen(Qt.PenStyle.NoPen)
                p.drawEllipse(cx-r-4, cy-r-4, (r+4)*2, (r+4)*2)
                col = accent.lighter(120) if hov else accent
                p.setBrush(QBrush(col)); p.setPen(QPen(accent.lighter(160), 2))
                p.drawEllipse(cx-r, cy-r, r*2, r*2)
                p.setPen(QPen(QColor(self._palette.get("accent_fg","#1e1e2e"))))
                p.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
                p.drawText(cx-r, cy-r, r*2, r*2, Qt.AlignmentFlag.AlignCenter,
                           str(step.step_number))
            else:
                col = QColor(self._palette.get("hover","#3b3d54")) if hov else surface
                p.setBrush(QBrush(col)); p.setPen(QPen(border, 1))
                p.drawEllipse(cx-r, cy-r, r*2, r*2)
                p.setPen(QPen(muted)); p.setFont(QFont("Segoe UI", 8))
                p.drawText(cx-r, cy-r, r*2, r*2, Qt.AlignmentFlag.AlignCenter,
                           str(step.step_number))
            p.setPen(QPen(muted if not active else accent))
            p.setFont(QFont("Segoe UI", 7))
            short = step.title[:14] + ("\u2026" if len(step.title) > 14 else "")
            p.drawText(cx-34, cy+r+6, 68, 16, Qt.AlignmentFlag.AlignCenter, short)
        p.end()

    def mouseMoveEvent(self, event):
        if not self._steps: return
        x = event.position().x(); old = self._hovered_idx
        self._hovered_idx = -1
        for i in range(len(self._steps)):
            if abs(x - self._node_cx(i)) <= 16:
                self._hovered_idx = i; break
        if self._hovered_idx != old: self.update()
        if self._hovered_idx >= 0:
            s   = self._steps[self._hovered_idx]
            tip = f"Step {s.step_number}: {s.title}\n{s.status.capitalize()}"
            if s.completed_at: tip += f"\nCompleted {s.completed_at[:10]}"
            self.setToolTip(tip)
        else: self.setToolTip("")

    def leaveEvent(self, _): self._hovered_idx = -1; self.update()

    def mousePressEvent(self, event):
        if not self._steps: return
        x = event.position().x()
        for i in range(len(self._steps)):
            if abs(x - self._node_cx(i)) <= 16:
                self.step_clicked.emit(i); return


class DomainBadge(QLabel):
    def __init__(self, domain: str, parent=None):
        super().__init__(domain, parent)
        self.setMinimumHeight(26)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.update_domain(domain)

    def update_domain(self, domain: str):
        self.setText(domain)
        c = DOMAIN_COLORS.get(domain, "#89dceb")
        self.setStyleSheet(
            f"QLabel{{background-color:{c}22;color:{c};"
            f"border:1px solid {c}66;border-radius:13px;"
            f"padding:4px 14px;font-size:11px;font-weight:bold;}}")


class _MiniProgressBar(QWidget):
    def __init__(self, done, total, color, track, parent=None):
        super().__init__(parent)
        self._done=done; self._total=max(total,1)
        self._color=QColor(color); self._track=QColor(track)
        self.setFixedHeight(4)

    def paintEvent(self, _):
        p=QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w=self.width()
        p.setBrush(QBrush(self._track)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(0, 0, w, 4, 2, 2)
        fw = int(w * self._done / self._total)
        if fw > 0:
            p.setBrush(QBrush(self._color)); p.drawRoundedRect(0, 0, fw, 4, 2, 2)
        p.end()


class ChecklistItem(QWidget):
    toggled = pyqtSignal(str, bool)

    def __init__(self, task: str, checked: bool, palette: dict, parent=None):
        super().__init__(parent)
        self._task = task; self._palette = palette
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 3, 0, 3); layout.setSpacing(10)
        self._cb = QCheckBox(); self._cb.setChecked(checked)
        self._cb.stateChanged.connect(
            lambda st: self.toggled.emit(self._task, st == Qt.CheckState.Checked.value))
        layout.addWidget(self._cb)
        lbl = QLabel(task); lbl.setWordWrap(True)
        lbl.setStyleSheet(self._task_style(checked, palette))
        self._lbl = lbl; layout.addWidget(lbl, 1)
        self._cb.stateChanged.connect(
            lambda st: self._lbl.setStyleSheet(
                self._task_style(st == Qt.CheckState.Checked.value, self._palette)))
        self._style_cb(palette)

    @staticmethod
    def _task_style(checked: bool, p: dict) -> str:
        c = p.get("muted","#7f849c") if checked else p.get("fg","#cdd6f4")
        d = "line-through" if checked else "none"
        return f"color:{c};font-size:12px;text-decoration:{d};"

    def _style_cb(self, p: dict):
        ac=p.get("accent","#89b4fa"); bd=p.get("border","#45475a"); sf=p.get("surface","#313244")
        self._cb.setStyleSheet(
            f"QCheckBox::indicator{{width:16px;height:16px;"
            f"border:1px solid {bd};border-radius:4px;background:{sf};}}"
            f"QCheckBox::indicator:checked{{background:{ac};border-color:{ac};}}"
            f"QCheckBox::indicator:hover{{border-color:{ac};}}")


class SectionCard(QFrame):
    def __init__(self, title: str, icon: str, palette: dict, parent=None):
        super().__init__(parent)
        p = palette
        self.setObjectName("SectionCard")
        self.setStyleSheet(
            f"QFrame#SectionCard{{background:{p.get('surface','#313244')};"
            f"border:1px solid {p.get('border','#45475a')};border-radius:10px;}}")
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(16, 12, 16, 14); self._layout.setSpacing(10)
        hdr = QHBoxLayout()
        il = QLabel(icon); il.setStyleSheet("font-size:16px;"); il.setFixedWidth(24)
        hdr.addWidget(il)
        tl = QLabel(title.upper())
        tl.setStyleSheet(
            f"color:{p.get('accent','#89b4fa')};font-size:10px;"
            f"font-weight:bold;letter-spacing:2px;")
        hdr.addWidget(tl); hdr.addStretch(); self._layout.addLayout(hdr)
        div = QFrame(); div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet(f"background:{p.get('border','#45475a')};max-height:1px;")
        self._layout.addWidget(div)

    def body_layout(self) -> QVBoxLayout:
        return self._layout


class CouncilorBadge(QWidget):
    def __init__(self, label: str, color: str, parent=None):
        super().__init__(parent)
        self._label = label; self._color = QColor(color); self.setFixedSize(32, 32)

    def paintEvent(self, _):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QBrush(self._color)); p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(0, 0, 32, 32)
        p.setPen(QPen(QColor("#ffffff")))
        p.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        initials = "".join(w[0] for w in self._label.split()[-2:])[:2].upper()
        p.drawText(0, 0, 32, 32, Qt.AlignmentFlag.AlignCenter, initials); p.end()


_COUNCILOR_COLORS = ["#89b4fa","#a6e3a1","#f5c2e7","#fab387",
                     "#94e2d5","#cba6f7","#89dceb","#f9e2af"]


class CouncilMemberCard(QFrame):
    def __init__(self, label: str, model: str, response: str,
                 color: str, palette: dict, parent=None):
        super().__init__(parent)
        self._expanded = False
        p = palette
        self.setObjectName("JourneyCouncilMember")
        self.setStyleSheet(
            f"QFrame#JourneyCouncilMember{{background:{p.get('bg','#1e1e2e')};"
            f"border:1px solid {p.get('border','#45475a')};border-radius:8px;margin:2px 0;}}")
        outer = QVBoxLayout(self); outer.setContentsMargins(10,8,10,8); outer.setSpacing(0)
        hdr = QHBoxLayout()
        hdr.addWidget(CouncilorBadge(label, color)); hdr.addSpacing(8)
        info = QVBoxLayout()
        nl = QLabel(label)
        nl.setStyleSheet(f"color:{p.get('fg','#cdd6f4')};font-weight:bold;font-size:12px;")
        sm = model.split("/")[-1].replace(":free","").replace(":nitro","")
        ml = QLabel(sm); ml.setStyleSheet(f"color:{p.get('muted','#7f849c')};font-size:10px;")
        info.addWidget(nl); info.addWidget(ml); hdr.addLayout(info); hdr.addStretch()
        self._toggle_btn = QToolButton()
        self._toggle_btn.setText("\u25b6  Show")
        self._toggle_btn.setStyleSheet(
            f"color:{p.get('muted','#7f849c')};font-size:10px;border:none;")
        self._toggle_btn.clicked.connect(self._toggle)
        hdr.addWidget(self._toggle_btn); outer.addLayout(hdr)
        self._browser = QTextBrowser()
        self._browser.setOpenExternalLinks(True)
        self._browser.setHtml(_to_html(response or "_No response._", palette))
        self._browser.setMinimumHeight(150); self._browser.setMaximumHeight(400)
        self._browser.hide()
        self._browser.setStyleSheet(
            f"QTextBrowser{{background:{p.get('surface','#313244')};"
            f"border:1px solid {p.get('border','#45475a')};border-radius:6px;"
            f"margin-top:8px;padding:6px;font-size:12px;}}")
        outer.addWidget(self._browser)

    def _toggle(self):
        self._expanded = not self._expanded
        self._browser.setVisible(self._expanded)
        self._toggle_btn.setText("\u25bc  Hide" if self._expanded else "\u25b6  Show")


class CouncilSessionCard(QFrame):
    def __init__(self, session: CouncilSession, session_num: int,
                 palette: dict, parent=None):
        super().__init__(parent)
        p = palette
        bg=p.get("bg","#1e1e2e"); surface=p.get("surface","#313244")
        border=p.get("border","#45475a"); muted=p.get("muted","#7f849c")
        accent=p.get("accent","#89b4fa"); green=p.get("green","#a6e3a1")
        bar = accent if session_num % 2 == 1 else green
        self.setObjectName("JourneySession")
        self.setStyleSheet(
            f"QFrame#JourneySession{{background:{surface};"
            f"border:1px solid {border};border-left:4px solid {bar};"
            f"border-radius:10px;margin:4px 0;}}")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14,12,14,12); layout.setSpacing(8)
        hdr = QHBoxLayout()
        sl = QLabel(f"\u2694  Session #{session_num}")
        sl.setStyleSheet(f"color:{bar};font-weight:bold;font-size:13px;")
        hdr.addWidget(sl); hdr.addStretch()
        ts = QLabel(session.created_at[:16].replace("T","  "))
        ts.setStyleSheet(f"color:{muted};font-size:10px;"); hdr.addWidget(ts)
        if session.web_search_used:
            wl = QLabel("\U0001f310 Web")
            wl.setStyleSheet(
                f"color:{green};font-size:10px;"
                f"border:1px solid {green}44;border-radius:8px;padding:1px 6px;")
            hdr.addSpacing(4); hdr.addWidget(wl)
        layout.addLayout(hdr)

        # Synthesis
        sl2 = QLabel("TUTOR SYNTHESIS")
        sl2.setStyleSheet(f"color:{muted};font-size:9px;font-weight:bold;letter-spacing:2px;")
        layout.addWidget(sl2)
        synth_text = session.synthesis.strip() or "_No synthesis content available._"
        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml(_to_html(synth_text, palette))
        browser.setMinimumHeight(260)
        browser.setStyleSheet(
            f"QTextBrowser{{background:{bg};border:1px solid {border};"
            f"border-radius:8px;padding:8px;font-size:12px;}}")
        layout.addWidget(browser)

        if session.web_search_queries:
            ql = QLabel("\U0001f50d " + " \u00b7 ".join(session.web_search_queries[:3]))
            ql.setStyleSheet(f"color:{muted};font-size:10px;font-style:italic;")
            ql.setWordWrap(True); layout.addWidget(ql)

        if session.member_records:
            n_v = len(session.member_records)
            vt  = QToolButton()
            vt.setText(f"\u25b6  Individual Model Responses  ({n_v})")
            vt.setStyleSheet(f"color:{muted};font-size:11px;border:none;padding:2px;")
            vt.setCheckable(True); layout.addWidget(vt)
            vc = QWidget(); vl = QVBoxLayout(vc)
            vl.setContentsMargins(0,4,0,0); vl.setSpacing(4); vc.hide()
            for j, rec in enumerate(session.member_records):
                color = _COUNCILOR_COLORS[j % len(_COUNCILOR_COLORS)]
                vl.addWidget(CouncilMemberCard(
                    rec.councilor_label, rec.model, rec.raw_response, color, palette))
            layout.addWidget(vc)
            def _tv(checked, c=vc, b=vt, n=n_v):
                c.setVisible(checked)
                b.setText(f"\u25bc  Individual Model Responses  ({n})" if checked
                          else f"\u25b6  Individual Model Responses  ({n})")
            vt.clicked.connect(_tv)


class HistoryStepRow(QFrame):
    def __init__(self, step: JourneyStep, palette: dict, parent=None):
        super().__init__(parent)
        p = palette
        self._expanded = False; self._has_notes = bool(step.user_notes)
        self.setObjectName("HistoryRow")
        self.setStyleSheet(
            f"QFrame#HistoryRow{{background:{p.get('alt_row','#252538')};"
            f"border:1px solid {p.get('border','#45475a')};border-radius:6px;}}"
            f"QFrame#HistoryRow:hover{{border-color:{p.get('muted','#7f849c')};}}")
        outer = QVBoxLayout(self); outer.setContentsMargins(10,6,10,6); outer.setSpacing(4)
        top = QHBoxLayout()
        icon = QLabel("\u2713"); icon.setStyleSheet(f"color:{p.get('green','#a6e3a1')};font-weight:bold;")
        top.addWidget(icon)
        tl = QLabel(f"Step {step.step_number}: {step.title}")
        tl.setStyleSheet(f"color:{p.get('muted','#7f849c')};font-size:11px;"); top.addWidget(tl, 1)
        if step.completed_at:
            dl = QLabel(step.completed_at[:10])
            dl.setStyleSheet(f"color:{p.get('muted','#7f849c')};font-size:10px;"); top.addWidget(dl)
        if self._has_notes:
            self._eb = QToolButton()
            self._eb.setText("\u25b6")
            self._eb.setStyleSheet(f"color:{p.get('muted','#7f849c')};font-size:9px;border:none;")
            self._eb.clicked.connect(self._toggle); top.addWidget(self._eb)
            self._nl = QLabel(step.user_notes[:400])
            self._nl.setStyleSheet(f"color:{p.get('fg','#cdd6f4')};font-size:11px;padding-left:18px;")
            self._nl.setWordWrap(True); self._nl.hide()
            outer.addLayout(top); outer.addWidget(self._nl)
        else:
            outer.addLayout(top)

    def _toggle(self):
        if not self._has_notes: return
        self._expanded = not self._expanded
        self._nl.setVisible(self._expanded)
        self._eb.setText("\u25bc" if self._expanded else "\u25b6")


class JourneyListItem(QFrame):
    clicked = pyqtSignal(str); archived = pyqtSignal(str)
    deleted = pyqtSignal(str); toggled_pause = pyqtSignal(str)

    def __init__(self, journey: Journey, palette: dict, parent=None):
        super().__init__(parent)
        self._journey_id=journey.id; self._journey=journey
        self._palette=palette; self._selected=False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style(False); self._build(journey)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _build(self, j: Journey):
        layout = QVBoxLayout(self); layout.setContentsMargins(10,9,10,9); layout.setSpacing(5)
        top = QHBoxLayout(); top.setSpacing(6)
        title = QLabel(j.title)
        title.setStyleSheet(
            f"color:{self._palette.get('fg','#cdd6f4')};font-weight:bold;font-size:12px;")
        title.setWordWrap(True); top.addWidget(title, 1)
        ICONS={"active":"\u2694","paused":"\u23f8","completed":"\U0001f3c6","archived":"\U0001f4e6"}
        si = QLabel(ICONS.get(j.status,""))
        si.setFixedWidth(20); si.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignRight)
        top.addWidget(si); layout.addLayout(top)
        if j.step_count > 0:
            layout.addWidget(_MiniProgressBar(j.completed_steps, j.step_count,
                             DOMAIN_COLORS.get(j.domain,"#89b4fa"),
                             self._palette.get("border","#45475a")))
        bot = QHBoxLayout(); bot.setSpacing(8)
        bot.addWidget(DomainBadge(j.domain)); bot.addStretch()
        steps_txt = f"{j.completed_steps}/{j.step_count} steps" if j.step_count > 0 else "no steps yet"
        pl = QLabel(steps_txt)
        pl.setStyleSheet(f"color:{self._palette.get('muted','#7f849c')};font-size:10px;")
        bot.addWidget(pl); layout.addLayout(bot)

    def _apply_style(self, selected: bool):
        p = self._palette
        bg = p.get("hover","#3b3d54") if selected else "transparent"
        bd = p.get("accent","#89b4fa") if selected else "transparent"
        self.setStyleSheet(f"QFrame{{background:{bg};border:1px solid {bd};border-radius:8px;}}")

    def set_selected(self, val: bool): self._selected = val; self._apply_style(val)
    def set_palette(self, palette: dict): self._palette = palette; self._apply_style(self._selected)
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._journey_id)

    def _show_context_menu(self, pos):
        p=self._palette; j=self._journey
        menu=QMenu(self)
        menu.setStyleSheet(
            f"QMenu{{background:{p.get('surface','#313244')};color:{p.get('fg','#cdd6f4')};"
            f"border:1px solid {p.get('border','#45475a')};border-radius:6px;padding:4px;}}"
            f"QMenu::item{{padding:5px 18px;border-radius:4px;}}"
            f"QMenu::item:selected{{background:{p.get('hover','#3b3d54')};}}")
        pl = "\u25b6  Resume Journey" if j.status=="paused" else "\u23f8  Pause Journey"
        pa=menu.addAction(pl); menu.addSeparator()
        ara=menu.addAction("\U0001f4e6  Archive Journey"); menu.addSeparator()
        da=menu.addAction("\U0001f5d1  Delete Journey")
        chosen=menu.exec(self.mapToGlobal(pos))
        if chosen==pa:  self.toggled_pause.emit(self._journey_id)
        elif chosen==ara: self.archived.emit(self._journey_id)
        elif chosen==da:  self.deleted.emit(self._journey_id)


# ── Dialogs ───────────────────────────────────────────────────────────────────

def _dialog_style(p: dict) -> str:
    return (
        f"QDialog{{background:{p.get('bg','#1e1e2e')};color:{p.get('fg','#cdd6f4')};}}"
        f"QLabel{{color:{p.get('fg','#cdd6f4')};font-size:12px;}}"
        f"QLineEdit,QTextEdit,QComboBox{{background:{p.get('surface','#313244')};"
        f"color:{p.get('fg','#cdd6f4')};border:1px solid {p.get('border','#45475a')};"
        f"border-radius:6px;padding:6px 8px;font-size:12px;}}"
        f"QLineEdit:focus,QTextEdit:focus{{border-color:{p.get('accent','#89b4fa')};}}"
        f"QPushButton{{background:{p.get('accent','#89b4fa')};"
        f"color:{p.get('accent_fg','#1e1e2e')};border:none;border-radius:6px;"
        f"padding:7px 18px;font-weight:bold;font-size:12px;}}"
        f"QPushButton:hover{{background:{p.get('accent_hover','#a0c5ff')};}}"
        f"QPushButton[secondary='true']{{background:{p.get('surface','#313244')};"
        f"color:{p.get('fg','#cdd6f4')};border:1px solid {p.get('border','#45475a')};"
        f"font-weight:normal;}}"
        f"QPushButton[secondary='true']:hover{{background:{p.get('hover','#3b3d54')};}}"
        f"QCheckBox{{color:{p.get('fg','#cdd6f4')};}}"
        f"QComboBox::drop-down{{border:none;}}"
        f"QComboBox QAbstractItemView{{background:{p.get('surface','#313244')};"
        f"color:{p.get('fg','#cdd6f4')};"
        f"selection-background-color:{p.get('hover','#3b3d60')};"
        f"border:1px solid {p.get('border','#45475a')};}}"
    )


class NewJourneyDialog(QDialog):
    def __init__(self, palette: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Journey"); self.setMinimumWidth(520)
        self.setModal(True); self.setStyleSheet(_dialog_style(palette))
        self._palette = palette; self._template_steps: list[str] = []
        self._build()

    def _build(self):
        layout = QVBoxLayout(self); layout.setSpacing(12); layout.setContentsMargins(20,20,20,20)

        tl = QLabel("Start from Template (optional)")
        tl.setStyleSheet(f"color:{self._palette.get('muted','#7f849c')};font-size:11px;font-style:italic;")
        layout.addWidget(tl)
        self._template_combo = QComboBox()
        self._template_combo.addItem("\u2014 Custom Journey \u2014")
        for name in JOURNEY_TEMPLATES:
            self._template_combo.addItem(name)
        self._template_combo.currentTextChanged.connect(self._on_template_changed)
        layout.addWidget(self._template_combo)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"background:{self._palette.get('border','#45475a')};")
        layout.addWidget(sep)

        layout.addWidget(QLabel("Journey Title"))
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("e.g. Learn Rust, Build a Freelance Pipeline\u2026")
        layout.addWidget(self.title_edit)

        layout.addWidget(QLabel("Domain"))
        self.domain_combo = QComboBox(); self.domain_combo.addItems(JOURNEY_DOMAINS)
        layout.addWidget(self.domain_combo)

        layout.addWidget(QLabel("Overall Goal / Description"))
        self.goal_edit = QTextEdit()
        self.goal_edit.setPlaceholderText(
            "Describe what you want to achieve. The more detail, the better the AI roadmap.\u2026")
        self.goal_edit.setFixedHeight(90); layout.addWidget(self.goal_edit)

        layout.addWidget(QLabel("First Step (optional \u2014 AI roadmap will suggest if blank)"))
        self.step_edit = QLineEdit()
        self.step_edit.setPlaceholderText("Leave blank to let the AI plan the first step")
        layout.addWidget(self.step_edit)

        self.web_check = QCheckBox("\U0001f310  Enable web search for council sessions")
        layout.addWidget(self.web_check)

        btn_row = QHBoxLayout()
        cancel = QPushButton("Cancel"); cancel.setProperty("secondary", True); cancel.clicked.connect(self.reject)
        create = QPushButton("\u2694  Begin Journey"); create.clicked.connect(self._accept)
        btn_row.addWidget(cancel); btn_row.addStretch(); btn_row.addWidget(create)
        layout.addLayout(btn_row)

    def _on_template_changed(self, name: str):
        t = JOURNEY_TEMPLATES.get(name)
        if not t: return
        self.title_edit.setText(name.split("(")[0].strip())
        idx = self.domain_combo.findText(t["domain"])
        if idx >= 0: self.domain_combo.setCurrentIndex(idx)
        self.goal_edit.setPlainText(t.get("goal",""))
        self._template_steps = t.get("steps",[])
        if self._template_steps: self.step_edit.setText(self._template_steps[0])

    def _accept(self):
        if not self.title_edit.text().strip(): self.title_edit.setFocus(); return
        self.accept()

    def get_data(self) -> dict:
        return {
            "title":          self.title_edit.text().strip(),
            "domain":         self.domain_combo.currentText(),
            "goal":           self.goal_edit.toPlainText().strip(),
            "first_step":     self.step_edit.text().strip(),
            "web_search":     self.web_check.isChecked(),
            "template_steps": self._template_steps,
        }


class AddStepDialog(QDialog):
    def __init__(self, palette: dict, title: str = "Add Step",
                 prefill_title: str = "", prefill_notes: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title); self.setMinimumWidth(480)
        self.setModal(True); self.setStyleSheet(_dialog_style(palette))
        self._pft = prefill_title; self._pfn = prefill_notes; self._build()

    def _build(self):
        layout = QVBoxLayout(self); layout.setSpacing(12); layout.setContentsMargins(20,20,20,20)
        layout.addWidget(QLabel("Step Title"))
        self.title_edit = QLineEdit(); self.title_edit.setPlaceholderText("What is this step called?")
        if self._pft: self.title_edit.setText(self._pft)
        layout.addWidget(self.title_edit)
        layout.addWidget(QLabel("Context / Lesson Focus (optional)"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText(
            "Describe what this step should cover. More detail → better tutoring.\u2026")
        self.notes_edit.setFixedHeight(90)
        if self._pfn: self.notes_edit.setPlainText(self._pfn)
        layout.addWidget(self.notes_edit)
        layout.addWidget(QLabel("Hints for Council (optional)"))
        self.hints_edit = QTextEdit()
        self.hints_edit.setPlaceholderText(
            "Specific angles, resources, or constraints for the council to focus on\u2026")
        self.hints_edit.setFixedHeight(70); layout.addWidget(self.hints_edit)
        btn_row = QHBoxLayout()
        cancel = QPushButton("Cancel"); cancel.setProperty("secondary", True); cancel.clicked.connect(self.reject)
        ok_btn = QPushButton("\u2694  Set Step"); ok_btn.clicked.connect(self._accept)
        btn_row.addWidget(cancel); btn_row.addStretch(); btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)

    def _accept(self):
        if not self.title_edit.text().strip(): self.title_edit.setFocus(); return
        self.accept()

    def get_data(self) -> dict:
        return {
            "title": self.title_edit.text().strip(),
            "notes": self.notes_edit.toPlainText().strip(),
            "hints": self.hints_edit.toPlainText().strip(),
        }


# ═══════════════════════════════════════════════════════════════════════════════
#  Main panel
# ═══════════════════════════════════════════════════════════════════════════════

class JourneyPanel(QWidget):

    def __init__(self, todo_store=None, calendar_store=None,
                 activity_store=None, notes_store=None, parent=None):
        super().__init__(parent)
        self._palette        = dict(_FALLBACK)
        self._todo_store     = todo_store
        self._calendar_store = calendar_store
        self._activity_store = activity_store
        self._notes_store    = notes_store
        self._store          = JourneyStore()

        self._active_journey:  Optional[Journey]     = None
        self._steps:           list[JourneyStep]     = []
        self._current_step:    Optional[JourneyStep] = None
        self._selected_rm_idx: int                   = -1   # selected roadmap node idx
        self._council_running: bool                  = False
        self._list_items:      list[JourneyListItem] = []
        self._save_timer:      Optional[QTimer]      = None
        self._checklist_state: dict                  = {}

        self._build_ui()
        self._refresh_journey_list()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        root = QHBoxLayout(self); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        splitter = QSplitter(Qt.Orientation.Horizontal); splitter.setHandleWidth(2)
        splitter.addWidget(self._build_left_panel())
        self._right_stack = QStackedWidget()
        self._right_stack.addWidget(self._build_empty_right())  # 0
        self._right_stack.addWidget(self._build_right_panel())  # 1
        splitter.addWidget(self._right_stack)
        splitter.setSizes([260, 820])
        splitter.setStretchFactor(0, 0); splitter.setStretchFactor(1, 1)
        root.addWidget(splitter)
        self._apply_palette(self._palette)

    def _build_left_panel(self) -> QWidget:
        w = QWidget(); w.setObjectName("JourneyLeft"); w.setMinimumWidth(240)
        layout = QVBoxLayout(w); layout.setContentsMargins(10,14,10,12); layout.setSpacing(8)
        hdr = QLabel("\u2694  JOURNEYS")
        hdr.setStyleSheet(
            f"color:{self._palette.get('accent','#89b4fa')};"
            f"font-size:12px;font-weight:bold;letter-spacing:2px;")
        layout.addWidget(hdr)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"background:{self._palette.get('border','#45475a')};max-height:1px;")
        layout.addWidget(sep)
        self._list_scroll = QScrollArea(); self._list_scroll.setWidgetResizable(True)
        self._list_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._list_container = QWidget()
        self._list_layout    = QVBoxLayout(self._list_container)
        self._list_layout.setContentsMargins(0,0,0,0); self._list_layout.setSpacing(4)
        self._list_layout.addStretch()
        self._list_scroll.setWidget(self._list_container)
        layout.addWidget(self._list_scroll, 1)
        self._new_btn = QPushButton("\uff0b  New Journey")
        self._new_btn.clicked.connect(self._on_new_journey)
        layout.addWidget(self._new_btn)
        return w

    def _build_empty_right(self) -> QWidget:
        w = QWidget(); layout = QVBoxLayout(w)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = QLabel("\U0001f5fa"); icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size:52px;")
        msg = QLabel("Select or create a journey\nto begin your quest.")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setStyleSheet(
            f"color:{self._palette.get('muted','#7f849c')};font-size:14px;")
        layout.addWidget(icon); layout.addSpacing(12); layout.addWidget(msg)
        return w

    def _build_right_panel(self) -> QWidget:
        w = QWidget(); outer = QVBoxLayout(w)
        outer.setContentsMargins(16,12,16,12); outer.setSpacing(8)
        outer.addWidget(self._build_journey_header())
        self._step_track = StepTrack()
        self._step_track.step_clicked.connect(self._on_step_track_clicked)
        outer.addWidget(self._step_track)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); outer.addWidget(sep)
        self._tabs = QTabWidget()
        self._tabs.addTab(self._build_overview_tab(),  "\U0001f4cb  Overview")
        self._tabs.addTab(self._build_council_tab(),   "\u2694  Council")
        self._tabs.addTab(self._build_workspace_tab(), "\u270f  Workspace")
        outer.addWidget(self._tabs, 1)
        return w

    def _build_journey_header(self) -> QWidget:
        w = QWidget(); w.setObjectName("JourneyHeader")
        layout = QVBoxLayout(w); layout.setContentsMargins(0,0,0,4); layout.setSpacing(6)
        self._title_label = QLabel("Journey")
        self._title_label.setStyleSheet(
            f"color:{self._palette.get('fg','#cdd6f4')};font-size:20px;font-weight:bold;")
        self._title_label.setWordWrap(True); layout.addWidget(self._title_label)
        meta = QHBoxLayout()
        self._domain_badge = DomainBadge("General"); meta.addWidget(self._domain_badge)
        meta.addSpacing(8)
        self._goal_label = QLabel("")
        self._goal_label.setStyleSheet(f"color:{self._palette.get('muted','#7f849c')};font-size:11px;")
        self._goal_label.setWordWrap(True); meta.addWidget(self._goal_label, 1)
        layout.addLayout(meta)
        ctrl = QHBoxLayout()
        self._web_toggle = QCheckBox("\U0001f310  Web Search")
        self._web_toggle.stateChanged.connect(self._on_web_toggle)
        ctrl.addWidget(self._web_toggle); ctrl.addStretch()
        self._pause_btn = QPushButton("\u23f8  Pause")
        self._pause_btn.setProperty("secondary", True); self._pause_btn.setFixedHeight(30)
        self._pause_btn.clicked.connect(self._on_toggle_pause)
        ctrl.addWidget(self._pause_btn); ctrl.addSpacing(6)
        self._complete_journey_btn = QPushButton("\U0001f3c6  Complete Journey")
        self._complete_journey_btn.setProperty("secondary", True)
        self._complete_journey_btn.setFixedHeight(30)
        self._complete_journey_btn.clicked.connect(self._on_complete_journey)
        ctrl.addWidget(self._complete_journey_btn); layout.addLayout(ctrl)
        return w

    # ── Overview tab ──────────────────────────────────────────────────────────

    def _build_overview_tab(self) -> QWidget:
        w = QWidget(); outer = QVBoxLayout(w)
        outer.setContentsMargins(0,8,0,0); outer.setSpacing(0)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        self._overview_layout = QVBoxLayout(content)
        self._overview_layout.setContentsMargins(4,4,4,8); self._overview_layout.setSpacing(14)
        self._overview_layout.addStretch()
        scroll.setWidget(content); outer.addWidget(scroll, 1)
        return w

    # ── Council tab ───────────────────────────────────────────────────────────

    def _build_council_tab(self) -> QWidget:
        w = QWidget(); outer = QVBoxLayout(w)
        outer.setContentsMargins(0,8,0,0); outer.setSpacing(0)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        self._council_layout = QVBoxLayout(content)
        self._council_layout.setContentsMargins(4,4,4,8); self._council_layout.setSpacing(8)
        self._sessions_label = QLabel("COUNCIL SESSIONS")
        self._sessions_label.setStyleSheet(
            f"color:{self._palette.get('muted','#7f849c')};"
            f"font-size:9px;font-weight:bold;letter-spacing:2px;")
        self._sessions_label.hide(); self._council_layout.addWidget(self._sessions_label)
        self._sessions_container = QWidget()
        self._sessions_layout = QVBoxLayout(self._sessions_container)
        self._sessions_layout.setContentsMargins(0,0,0,0); self._sessions_layout.setSpacing(8)
        self._council_layout.addWidget(self._sessions_container)
        self._history_label = QLabel("QUEST LOG \u2014 COMPLETED STEPS")
        self._history_label.setStyleSheet(
            f"color:{self._palette.get('muted','#7f849c')};"
            f"font-size:9px;font-weight:bold;letter-spacing:2px;margin-top:8px;")
        self._history_label.hide(); self._council_layout.addWidget(self._history_label)
        self._history_container = QWidget()
        self._history_layout = QVBoxLayout(self._history_container)
        self._history_layout.setContentsMargins(0,0,0,0); self._history_layout.setSpacing(4)
        self._council_layout.addWidget(self._history_container)
        self._council_layout.addStretch()
        scroll.setWidget(content); outer.addWidget(scroll, 1)
        return w

    # ── Workspace tab ─────────────────────────────────────────────────────────

    def _build_workspace_tab(self) -> QWidget:
        w = QWidget(); outer = QVBoxLayout(w)
        outer.setContentsMargins(0,8,0,0); outer.setSpacing(0)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(4,4,4,8); layout.setSpacing(12)

        card = QFrame(); card.setObjectName("JourneyStepCard")
        sc = QVBoxLayout(card); sc.setContentsMargins(20,18,20,18); sc.setSpacing(12)

        tr = QHBoxLayout(); tr.setSpacing(10)
        self._step_icon = QLabel("\U0001f4dc")
        self._step_icon.setStyleSheet("font-size:22px;"); self._step_icon.setFixedWidth(30)
        self._step_icon.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignHCenter)
        tr.addWidget(self._step_icon)
        tc = QVBoxLayout(); tc.setSpacing(3)
        self._step_num_label = QLabel("")
        self._step_num_label.setStyleSheet(
            f"color:{self._palette.get('muted','#7f849c')};"
            f"font-size:9px;font-weight:bold;letter-spacing:2px;")
        self._step_title_label = QLabel("No active step")
        self._step_title_label.setStyleSheet(
            f"color:{self._palette.get('accent','#89b4fa')};font-size:16px;font-weight:bold;")
        self._step_title_label.setWordWrap(True)
        self._step_title_label.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        tc.addWidget(self._step_num_label); tc.addWidget(self._step_title_label)
        tr.addLayout(tc, 1); sc.addLayout(tr)

        div = QFrame(); div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet(f"background:{self._palette.get('border','#45475a')};max-height:1px;")
        sc.addWidget(div)

        sc.addWidget(self._mklbl("LESSON NOTES & PROGRESS"))
        self._notes_edit = QTextEdit()
        self._notes_edit.setPlaceholderText(
            "Record what you're learning, questions, code you're writing, "
            "breakthroughs, and blockers. The more detail, the better the council "
            "can guide your next step\u2026")
        self._notes_edit.setMinimumHeight(160)
        self._notes_edit.textChanged.connect(self._auto_save_notes)
        sc.addWidget(self._notes_edit)

        sc.addWidget(self._mklbl("HINTS FOR COUNCIL  \u2014  optional"))
        self._hints_edit = QTextEdit()
        self._hints_edit.setPlaceholderText(
            "Specific angles, resources, or constraints to focus on\u2026")
        self._hints_edit.setMinimumHeight(100)
        self._hints_edit.textChanged.connect(self._auto_save_notes)
        sc.addWidget(self._hints_edit)

        # Primary actions
        btn_row = QHBoxLayout(); btn_row.setSpacing(10)
        self._council_btn = QPushButton("\u2694  Convene Council")
        self._council_btn.setFixedHeight(44)
        self._council_btn.clicked.connect(self._on_convene_council)
        btn_row.addWidget(self._council_btn, 3)
        self._complete_btn = QPushButton("\u2713  Complete & Next Step")
        self._complete_btn.setProperty("secondary", True); self._complete_btn.setFixedHeight(44)
        self._complete_btn.clicked.connect(self._on_complete_step)
        btn_row.addWidget(self._complete_btn, 2)
        sc.addLayout(btn_row)

        # Add step / update roadmap row
        aux_row = QHBoxLayout(); aux_row.setSpacing(8)
        self._add_step_btn = QPushButton("\uff0b  Add New Step")
        self._add_step_btn.setProperty("secondary", True); self._add_step_btn.setFixedHeight(36)
        self._add_step_btn.clicked.connect(self._on_add_step); self._add_step_btn.hide()
        aux_row.addWidget(self._add_step_btn)
        aux_row.addStretch()
        self._update_rm_btn = QPushButton("\U0001f504  Update Roadmap")
        self._update_rm_btn.setProperty("secondary", True); self._update_rm_btn.setFixedHeight(36)
        self._update_rm_btn.setToolTip(
            "Send your current notes/hints to the AI to update the journey roadmap")
        self._update_rm_btn.clicked.connect(self._on_update_roadmap)
        aux_row.addWidget(self._update_rm_btn)
        sc.addLayout(aux_row)

        # Progress/status line
        self._council_status = QLabel("")
        self._council_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._council_status.setStyleSheet(
            f"color:{self._palette.get('muted','#7f849c')};"
            f"font-size:11px;font-style:italic;padding:4px 0;")
        self._council_status.hide(); sc.addWidget(self._council_status)

        layout.addWidget(card); layout.addStretch()
        scroll.setWidget(content); outer.addWidget(scroll, 1)
        return w

    def _mklbl(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"color:{self._palette.get('muted','#7f849c')};"
            f"font-size:9px;font-weight:bold;letter-spacing:2px;")
        return lbl

    # ── Palette ───────────────────────────────────────────────────────────────

    def set_palette(self, palette: dict):
        self._palette = palette
        self._apply_palette(palette)
        if self._current_step or self._active_journey:
            self._refresh_overview()
            self._refresh_sessions()
            self._refresh_history()

    def _apply_palette(self, p: dict):
        bg=p.get("bg","#1e1e2e"); surface=p.get("surface","#313244")
        border=p.get("border","#45475a"); fg=p.get("fg","#cdd6f4")
        muted=p.get("muted","#7f849c"); accent=p.get("accent","#89b4fa")
        accent_fg=p.get("accent_fg","#1e1e2e"); accent_h=p.get("accent_hover","#a0c5ff")
        accent_pr=p.get("accent_pressed","#74a4ea"); green=p.get("green","#a6e3a1")
        hover=p.get("hover","#3b3d54"); header_bg=p.get("header_bg",bg)

        self.setStyleSheet(
            f"QWidget#JourneyLeft{{background:{header_bg};border-right:1px solid {border};}}"
            f"QFrame#JourneyStepCard{{background:{surface};border:1px solid {border};"
            f"border-left:4px solid {accent};border-radius:10px;}}"
            f"QTextEdit{{background:{bg};color:{fg};border:1px solid {border};"
            f"border-radius:6px;padding:8px;font-size:13px;"
            f"selection-background-color:{accent};selection-color:{accent_fg};}}"
            f"QTextEdit:focus{{border-color:{accent};}}"
            f"QScrollArea{{background:transparent;border:none;}}"
            f"QScrollBar:vertical{{background:{bg};width:6px;border-radius:3px;}}"
            f"QScrollBar::handle:vertical{{background:{border};border-radius:3px;min-height:20px;}}"
            f"QScrollBar::handle:vertical:hover{{background:{muted};}}"
            f"QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}"
            f"QScrollBar:horizontal{{background:{bg};height:6px;border-radius:3px;}}"
            f"QScrollBar::handle:horizontal{{background:{border};border-radius:3px;min-width:20px;}}"
            f"QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{{width:0;}}"
            f"QPushButton{{background:{accent};color:{accent_fg};border:none;"
            f"border-radius:6px;padding:6px 16px;font-size:12px;font-weight:bold;}}"
            f"QPushButton:hover{{background:{accent_h};}}"
            f"QPushButton:pressed{{background:{accent_pr};}}"
            f"QPushButton:disabled{{background:{border};color:{muted};}}"
            f"QPushButton[secondary='true']{{background:{surface};color:{fg};"
            f"border:1px solid {border};font-weight:normal;}}"
            f"QPushButton[secondary='true']:hover{{background:{hover};}}"
            f"QFrame[frameShape='4']{{background:{border};max-height:1px;}}"
            f"QCheckBox{{color:{fg};font-size:11px;}}"
            f"QCheckBox::indicator{{width:14px;height:14px;border:1px solid {border};"
            f"border-radius:3px;background:{surface};}}"
            f"QCheckBox::indicator:checked{{background:{accent};border-color:{accent};}}"
            f"QSplitter::handle{{background:{border};}}"
            f"QToolButton{{color:{muted};font-size:11px;border:none;"
            f"background:transparent;padding:2px;}}"
            f"QToolButton:hover{{color:{fg};}}"
        )
        if hasattr(self, "_tabs"):          self._tabs.setStyleSheet(_tab_style(p))
        if hasattr(self, "_step_track"):    self._step_track.set_palette(p)
        if hasattr(self, "_roadmap_widget"):self._roadmap_widget.set_palette(p)
        if hasattr(self, "_title_label"):
            self._title_label.setStyleSheet(f"color:{fg};font-size:20px;font-weight:bold;")
        if hasattr(self, "_goal_label"):
            self._goal_label.setStyleSheet(f"color:{muted};font-size:11px;")
        if hasattr(self, "_step_num_label"):
            self._step_num_label.setStyleSheet(
                f"color:{muted};font-size:9px;font-weight:bold;letter-spacing:2px;")
        if hasattr(self, "_step_title_label"):
            self._step_title_label.setStyleSheet(
                f"color:{accent};font-size:16px;font-weight:bold;")
        if hasattr(self, "_council_btn"):
            self._council_btn.setStyleSheet(
                f"QPushButton{{background:qlineargradient("
                f"x1:0,y1:0,x2:1,y2:0,stop:0 {accent},stop:1 {green});"
                f"color:{accent_fg};border:none;border-radius:8px;"
                f"font-size:13px;font-weight:bold;padding:0 18px;}}"
                f"QPushButton:hover{{background:qlineargradient("
                f"x1:0,y1:0,x2:1,y2:0,stop:0 {accent_h},stop:1 {green});}}"
                f"QPushButton:disabled{{background:{border};color:{muted};}}")
        for item in self._list_items:
            item.set_palette(p)

    # ── Journey list ──────────────────────────────────────────────────────────

    def _refresh_journey_list(self):
        while self._list_layout.count():
            item = self._list_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._list_items.clear()
        for j in self._store.list_journeys():
            item = JourneyListItem(j, self._palette)
            item.clicked.connect(self._on_journey_selected)
            item.archived.connect(self._on_archive_journey)
            item.deleted.connect(self._on_delete_journey)
            item.toggled_pause.connect(self._on_toggle_pause_by_id)
            self._list_layout.addWidget(item); self._list_items.append(item)
        self._list_layout.addStretch()
        if self._active_journey: self._mark_selected(self._active_journey.id)

    def _mark_selected(self, journey_id: str):
        for item in self._list_items:
            item.set_selected(item._journey_id == journey_id)

    # ── Journey loading ───────────────────────────────────────────────────────

    def _on_journey_selected(self, journey_id: str):
        journey = self._store.get_journey(journey_id)
        if not journey: return
        self._active_journey = journey
        self._mark_selected(journey_id); self._load_journey(journey)

    def _load_journey(self, journey: Journey):
        self._title_label.setText(journey.title)
        goal = journey.goal_description
        self._goal_label.setText(goal[:130] + ("\u2026" if len(goal)>130 else ""))
        self._domain_badge.update_domain(journey.domain)
        is_paused = journey.status == "paused"
        self._pause_btn.setText("\u25b6  Resume" if is_paused else "\u23f8  Pause")
        self._pause_btn.setEnabled(journey.status in ("active","paused"))
        self._complete_journey_btn.setEnabled(journey.status not in ("completed","archived"))
        self._web_toggle.blockSignals(True)
        self._web_toggle.setChecked(journey.web_search_enabled)
        self._web_toggle.blockSignals(False)
        self._steps = self._store.list_steps(journey.id)
        self._step_track.set_steps(self._steps)
        active = [s for s in self._steps if s.status == "active"]
        self._current_step = active[0] if active else None
        self._checklist_state = dict(self._current_step.checklist_state) if self._current_step else {}
        # Auto-select current step in roadmap
        if self._current_step:
            roadmap = journey.roadmap
            for i, rs in enumerate(roadmap.steps):
                if rs.title.strip().lower() == self._current_step.title.strip().lower():
                    self._selected_rm_idx = i
                    break
        else:
            self._selected_rm_idx = -1
        self._refresh_workspace()
        self._refresh_overview()
        self._refresh_sessions()
        self._refresh_history()
        self._right_stack.setCurrentIndex(1)

    def _refresh_workspace(self):
        step = self._current_step; total = len(self._steps)
        if step:
            self._step_num_label.setText(f"STEP {step.step_number} OF {total}")
            self._step_title_label.setText(step.title)
            self._notes_edit.blockSignals(True)
            self._notes_edit.setPlainText(step.user_notes)
            self._notes_edit.blockSignals(False)
            self._hints_edit.blockSignals(True)
            self._hints_edit.setPlainText(step.user_next_suggestions)
            self._hints_edit.blockSignals(False)
            self._notes_edit.setEnabled(True); self._hints_edit.setEnabled(True)
            self._council_btn.setEnabled(True); self._council_btn.show()
            self._complete_btn.setEnabled(True); self._complete_btn.show()
            self._add_step_btn.hide(); self._step_icon.setText("\U0001f4dc")
        else:
            if total > 0:
                self._step_num_label.setText(f"ALL {total} STEPS COMPLETE")
                self._step_title_label.setText("Add a new step or click a roadmap node.")
                self._step_icon.setText("\U0001f3c6")
            else:
                self._step_num_label.setText("NO STEPS YET")
                self._step_title_label.setText("Add your first step below.")
                self._step_icon.setText("\U0001f4cb")
            self._notes_edit.clear(); self._notes_edit.setEnabled(False)
            self._hints_edit.clear(); self._hints_edit.setEnabled(False)
            self._council_btn.hide(); self._complete_btn.hide()
            self._add_step_btn.show()

    # ── Overview tab ──────────────────────────────────────────────────────────

    def _refresh_overview(self):
        while self._overview_layout.count():
            item = self._overview_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        p       = self._palette
        journey = self._active_journey
        if not journey:
            self._overview_layout.addStretch(); return

        roadmap = journey.roadmap

        # ── Roadmap card ───────────────────────────────────────────────────────
        if roadmap.steps:
            rm_card = SectionCard("Journey Roadmap", "\U0001f5fa", p)
            bl = rm_card.body_layout()
            if roadmap.overview:
                ov = QLabel(roadmap.overview)
                ov.setStyleSheet(f"color:{p.get('muted','#7f849c')};font-size:12px;font-style:italic;")
                ov.setWordWrap(True); bl.addWidget(ov)

            # The roadmap widget in a horizontal scroll area
            h_scroll = QScrollArea()
            h_scroll.setWidgetResizable(False)
            h_scroll.setFrameShape(QFrame.Shape.NoFrame)
            h_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            h_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            h_scroll.setStyleSheet("QScrollArea{background:transparent;border:none;}")

            self._roadmap_widget = RoadmapWidget()
            self._roadmap_widget.set_palette(p)
            self._roadmap_widget.set_data(roadmap, self._steps, self._selected_rm_idx)
            self._roadmap_widget.node_selected.connect(self._on_roadmap_node_selected)
            h_scroll.setWidget(self._roadmap_widget)
            h_scroll.setFixedHeight(self._roadmap_widget.minimumHeight() + 6)
            bl.addWidget(h_scroll)

            # Detour legend
            if any(rs.is_detour for rs in roadmap.steps):
                dl = QLabel(
                    f"\U0001f7e8 = Detour step (off original plan)")
                dl.setStyleSheet(f"color:{p.get('yellow','#f9e2af')};font-size:10px;")
                bl.addWidget(dl)

            self._overview_layout.addWidget(rm_card)

            # ── Selected node detail card ──────────────────────────────────────
            if 0 <= self._selected_rm_idx < len(roadmap.steps):
                rs = roadmap.steps[self._selected_rm_idx]
                self._build_selected_step_card(rs, p)

        elif not self._current_step:
            ph = QLabel(
                "\u2694  Create and begin a step, then convene the council\n"
                "to generate your tutoring session, checklist, and roadmap.")
            ph.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ph.setStyleSheet(f"color:{p.get('muted','#7f849c')};font-size:13px;padding:20px;")
            self._overview_layout.addWidget(ph)
            self._overview_layout.addStretch()
            return

        # ── Council content for current step ──────────────────────────────────
        if not self._current_step:
            self._overview_layout.addStretch(); return

        sessions = self._store.list_sessions_for_step(self._current_step.id)
        if not sessions:
            no_sess = QLabel(
                "\u270f  Go to the Workspace tab and click\n"
                "\u2694 Convene Council to generate your tutoring session.")
            no_sess.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_sess.setStyleSheet(
                f"color:{p.get('muted','#7f849c')};font-size:13px;padding:20px;")
            self._overview_layout.addWidget(no_sess)
            self._overview_layout.addStretch()
            return

        latest = sessions[-1]
        synth  = (latest.synthesis or "").strip()

        # Synthesis card — always shown, even if empty (shows error message)
        syn_card = SectionCard("Council Tutoring Session", "\u2694", p)
        bl2 = syn_card.body_layout()
        display_text = synth if synth else (
            "_The council completed but returned no synthesis content.\n"
            "Check your model configuration, or convene again._"
        )
        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml(_to_html(display_text, p))
        browser.setMinimumHeight(360)
        browser.setStyleSheet(
            f"QTextBrowser{{background:{p.get('bg','#1e1e2e')};"
            f"border:none;border-radius:6px;padding:4px;font-size:12px;}}")
        bl2.addWidget(browser)
        self._overview_layout.addWidget(syn_card)

        # 2-col: checklist + next steps from roadmap
        row_w = QWidget(); row = QHBoxLayout(row_w)
        row.setContentsMargins(0,0,0,0); row.setSpacing(12)

        if latest.step_checklist:
            cl_card = SectionCard("Action Checklist", "\u2714", p)
            for task in latest.step_checklist:
                checked = self._checklist_state.get(task, False)
                ci = ChecklistItem(task, checked, p)
                ci.toggled.connect(self._on_checklist_toggled)
                cl_card.body_layout().addWidget(ci)
            row.addWidget(cl_card, 3)

        next_rs = self._get_next_roadmap_steps(2)
        if next_rs:
            ns_card = SectionCard("Up Next from Roadmap", "\u27a1", p)
            ns_bl = ns_card.body_layout()
            for rs in next_rs:
                btn = QPushButton(f"  {rs.number}. {rs.title}")
                btn.setProperty("secondary", True); btn.setFixedHeight(38)
                btn.setStyleSheet(
                    f"QPushButton{{background:{p.get('surface','#313244')};"
                    f"color:{p.get('fg','#cdd6f4')};border:1px solid {p.get('border','#45475a')};"
                    f"border-left:3px solid {p.get('accent','#89b4fa')};"
                    f"border-radius:6px;text-align:left;padding-left:12px;font-size:12px;}}"
                    f"QPushButton:hover{{background:{p.get('hover','#3b3d54')};}}")
                btn.clicked.connect(lambda _, r=rs: self._on_roadmap_step_clicked(r))
                ns_bl.addWidget(btn)
                if rs.description:
                    dl = QLabel(rs.description[:90] + ("\u2026" if len(rs.description)>90 else ""))
                    dl.setStyleSheet(f"color:{p.get('muted','#7f849c')};font-size:10px;padding-left:12px;")
                    dl.setWordWrap(True); ns_bl.addWidget(dl)
            row.addWidget(ns_card, 2)

        if latest.step_checklist or next_rs:
            self._overview_layout.addWidget(row_w)

        if latest.step_resources:
            rc = SectionCard("Resources & References", "\U0001f4da", p)
            for res in latest.step_resources:
                rl = QLabel(f"\u2022  {res}")
                rl.setStyleSheet(f"color:{p.get('fg','#cdd6f4')};font-size:12px;")
                rl.setWordWrap(True); rc.body_layout().addWidget(rl)
            self._overview_layout.addWidget(rc)

        if latest.roadmap_text:
            nc = SectionCard("What Comes Next", "\U0001f5fa", p)
            nl = QLabel(latest.roadmap_text)
            nl.setStyleSheet(f"color:{p.get('fg','#cdd6f4')};font-size:12px;line-height:1.7;")
            nl.setWordWrap(True); nc.body_layout().addWidget(nl)
            self._overview_layout.addWidget(nc)

        # Footer
        fw = QWidget(); fl = QHBoxLayout(fw); fl.setContentsMargins(0,0,0,0)
        ts_lbl = QLabel(
            f"Session #{len(sessions)}  \u00b7  "
            f"{latest.created_at[:16].replace('T','  ')}")
        ts_lbl.setStyleSheet(f"color:{p.get('muted','#7f849c')};font-size:10px;")
        fl.addWidget(ts_lbl); fl.addStretch()
        regen_btn = QPushButton("\u21bb  Regenerate Plan")
        regen_btn.setProperty("secondary", True); regen_btn.setFixedHeight(28)
        regen_btn.clicked.connect(self._on_regen_overview); fl.addWidget(regen_btn)
        self._overview_layout.addWidget(fw)
        self._overview_layout.addStretch()

    def _build_selected_step_card(self, rs: RoadmapStep, p: dict):
        """Show the selected roadmap step's detail below the flow."""
        card = SectionCard(f"Step {rs.number}: {rs.title}",
                           "\U0001f4cc" if rs.is_detour else "\U0001f4cd", p)
        bl = card.body_layout()

        if rs.description:
            dl = QLabel(rs.description)
            dl.setStyleSheet(f"color:{p.get('fg','#cdd6f4')};font-size:12px;")
            dl.setWordWrap(True); bl.addWidget(dl)

        if rs.objectives:
            obj_lbl = QLabel("OBJECTIVES")
            obj_lbl.setStyleSheet(
                f"color:{p.get('muted','#7f849c')};font-size:9px;"
                f"font-weight:bold;letter-spacing:2px;")
            bl.addWidget(obj_lbl)
            for obj in rs.objectives:
                ol = QLabel(f"  \u2022  {obj}")
                ol.setStyleSheet(f"color:{p.get('fg','#cdd6f4')};font-size:12px;")
                ol.setWordWrap(True); bl.addWidget(ol)

        if rs.is_detour:
            det_lbl = QLabel("\U0001f7e8  This is a detour step — added outside the original plan.")
            det_lbl.setStyleSheet(f"color:{p.get('yellow','#f9e2af')};font-size:11px;font-style:italic;")
            bl.addWidget(det_lbl)

        # Action button
        step_status = "unstarted"
        for s in self._steps:
            if s.title.strip().lower() == rs.title.strip().lower():
                step_status = s.status; break

        btn_row = QHBoxLayout()
        if step_status == "unstarted":
            begin_btn = QPushButton(f"\u2694  Begin Step {rs.number}: {rs.title[:40]}")
            begin_btn.setFixedHeight(40)
            begin_btn.clicked.connect(lambda _, r=rs: self._on_begin_roadmap_step(r))
            btn_row.addWidget(begin_btn)
        elif step_status == "active":
            ws_btn = QPushButton("\u270f  Go to Workspace")
            ws_btn.setFixedHeight(40)
            ws_btn.clicked.connect(lambda: self._tabs.setCurrentIndex(_TAB_WORKSPACE))
            btn_row.addWidget(ws_btn)
        else:
            done_lbl = QLabel("\u2713  Step completed")
            done_lbl.setStyleSheet(f"color:{p.get('green','#a6e3a1')};font-size:13px;font-weight:bold;")
            btn_row.addWidget(done_lbl)
        btn_row.addStretch()
        bl.addLayout(btn_row)
        self._overview_layout.addWidget(card)

    def _get_next_roadmap_steps(self, count: int = 2) -> list[RoadmapStep]:
        if not self._active_journey: return []
        started = {s.title.strip().lower() for s in self._steps}
        return [rs for rs in self._active_journey.roadmap.steps
                if rs.title.strip().lower() not in started][:count]

    # ── Council tab ───────────────────────────────────────────────────────────

    def _refresh_sessions(self):
        while self._sessions_layout.count():
            item = self._sessions_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        if not self._current_step:
            self._sessions_label.hide(); return
        sessions = self._store.list_sessions_for_step(self._current_step.id)
        if not sessions:
            self._sessions_label.hide(); return
        self._sessions_label.show()
        for i, session in enumerate(reversed(sessions)):
            num = len(sessions) - i
            self._sessions_layout.addWidget(
                CouncilSessionCard(session, num, self._palette))

    def _refresh_history(self):
        while self._history_layout.count():
            item = self._history_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        done = [s for s in self._steps if s.status == "completed"]
        if not done: self._history_label.hide(); return
        self._history_label.show()
        for step in reversed(done):
            self._history_layout.addWidget(HistoryStepRow(step, self._palette))

    # ── Checklist ─────────────────────────────────────────────────────────────

    def _on_checklist_toggled(self, task: str, checked: bool):
        self._checklist_state[task] = checked
        if self._current_step:
            self._store.update_checklist_state(self._current_step.id,
                                               self._checklist_state)

    # ── Auto-save ─────────────────────────────────────────────────────────────

    def _auto_save_notes(self):
        if not self._current_step: return
        if self._save_timer is None:
            self._save_timer = QTimer(self)
            self._save_timer.setSingleShot(True)
            self._save_timer.timeout.connect(self._flush_notes)
        self._save_timer.start(1200)

    def _flush_notes(self):
        if not self._current_step: return
        self._store.update_step_notes(
            self._current_step.id,
            self._notes_edit.toPlainText(),
            self._hints_edit.toPlainText())

    # ── Roadmap interaction ───────────────────────────────────────────────────

    def _on_roadmap_node_selected(self, idx: int):
        """Node clicked in the flow widget — update selection and refresh detail."""
        self._selected_rm_idx = idx
        self._refresh_overview()
        # Also sync step track if the clicked node corresponds to an actual step
        if self._active_journey and 0 <= idx < len(self._active_journey.roadmap.steps):
            rs = self._active_journey.roadmap.steps[idx]
            for i, s in enumerate(self._steps):
                if s.title.strip().lower() == rs.title.strip().lower():
                    # Activate that step's council content if it exists
                    break

    def _on_begin_roadmap_step(self, rs: RoadmapStep):
        """User clicked 'Begin Step N' in the selected-step detail card."""
        if not self._active_journey: return
        desc = rs.description
        if rs.objectives:
            desc += "\n\nObjectives:\n" + "\n".join(f"\u2022 {o}" for o in rs.objectives)
        dlg = AddStepDialog(self._palette, title=f"Begin: {rs.title}",
                            prefill_title=rs.title, prefill_notes=desc, parent=self)
        if dlg.exec() != QDialog.DialogCode.Accepted: return
        data = dlg.get_data()

        # If there's a current active step, warn the user
        if self._current_step and self._current_step.status == "active":
            reply = QMessageBox.question(
                self, "Active Step Exists",
                f"You already have an active step: \"{self._current_step.title}\".\n\n"
                "Creating a new step will not complete the current one. Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            if reply != QMessageBox.StandardButton.Yes: return

        new_step = self._store.create_step(
            self._active_journey.id, title=data["title"],
            user_notes=data["notes"], suggestions=data["hints"])

        # If this step is not in the roadmap, mark it as a detour
        roadmap = self._active_journey.roadmap
        if not roadmap.get_step_by_title(data["title"]):
            roadmap.add_detour_step(data["title"], data["notes"],
                                    branch_from=self._current_step.step_number
                                    if self._current_step else None)
            self._store.update_roadmap(self._active_journey.id, roadmap)

        self._steps = self._store.list_steps(self._active_journey.id)
        self._step_track.set_steps(self._steps)
        self._current_step = new_step; self._checklist_state = {}
        self._selected_rm_idx = idx_of_step(new_step, self._active_journey.roadmap)
        self._active_journey = self._store.get_journey(self._active_journey.id)
        self._refresh_workspace(); self._refresh_sessions()
        self._refresh_overview(); self._refresh_journey_list()
        # Switch to Workspace so user can review and manually convene when ready
        self._tabs.setCurrentIndex(_TAB_WORKSPACE)

    def _on_roadmap_step_clicked(self, rs: RoadmapStep):
        """'Up Next' button clicked — open AddStepDialog pre-filled."""
        if not self._active_journey: return
        desc = rs.description
        if rs.objectives:
            desc += "\n\nObjectives:\n" + "\n".join(f"\u2022 {o}" for o in rs.objectives)
        dlg = AddStepDialog(self._palette, title="Start Next Step",
                            prefill_title=rs.title, prefill_notes=desc, parent=self)
        if dlg.exec() != QDialog.DialogCode.Accepted: return
        data = dlg.get_data()
        new_step = self._store.create_step(
            self._active_journey.id, title=data["title"],
            user_notes=data["notes"], suggestions=data["hints"])
        self._steps = self._store.list_steps(self._active_journey.id)
        self._step_track.set_steps(self._steps)
        self._current_step = new_step; self._checklist_state = {}
        self._selected_rm_idx = idx_of_step(new_step, self._active_journey.roadmap)
        self._refresh_workspace(); self._refresh_sessions()
        self._refresh_overview(); self._refresh_journey_list()
        self._tabs.setCurrentIndex(_TAB_WORKSPACE)

    # ── Actions ───────────────────────────────────────────────────────────────

    def _on_new_journey(self):
        dlg = NewJourneyDialog(self._palette, self)
        if dlg.exec() != QDialog.DialogCode.Accepted: return
        data    = dlg.get_data()
        journey = self._store.create_journey(
            title=data["title"], goal=data["goal"],
            domain=data["domain"], web_search=data["web_search"])
        self._refresh_journey_list()
        self._on_journey_selected(journey.id)

        llm_client = load_llm_client()
        if not llm_client:
            # No LLM — create first step from dialog if given
            if data["first_step"]:
                self._store.create_step(journey.id, title=data["first_step"])
                self._on_journey_selected(journey.id)
            return

        # Generate roadmap in background — no auto-convene, no auto step creation
        template_steps = data.get("template_steps", [])
        first_step_title = data["first_step"]

        def _gen_roadmap():
            # Use fresh journey object for roadmap generation
            fresh = self._store.get_journey(journey.id)
            if not fresh: return
            roadmap = _generate_roadmap(llm_client, fresh)
            if not roadmap.steps:
                # Fallback: build from template steps
                if template_steps:
                    roadmap = Roadmap(
                        overview="Learning path based on template.",
                        steps=[RoadmapStep(number=i+1, title=t, description="")
                               for i, t in enumerate(template_steps)])
            if roadmap.steps:
                self._store.update_roadmap(journey.id, roadmap)
            # Reload in main thread — NO step creation, NO auto-convene
            QTimer.singleShot(0, lambda: self._on_journey_selected(journey.id))

        threading.Thread(target=_gen_roadmap, daemon=True).start()

    def _on_add_step(self):
        if not self._active_journey: return
        next_rs = self._get_next_roadmap_steps(1)
        pft = next_rs[0].title if next_rs else ""
        pfn = ""
        if next_rs:
            rs = next_rs[0]
            pfn = rs.description
            if rs.objectives:
                pfn += "\n\nObjectives:\n" + "\n".join(f"\u2022 {o}" for o in rs.objectives)
        dlg = AddStepDialog(self._palette, title="Add Step",
                            prefill_title=pft, prefill_notes=pfn, parent=self)
        if dlg.exec() != QDialog.DialogCode.Accepted: return
        data = dlg.get_data()
        # Check if this step is in the roadmap; if not, record as detour
        roadmap = self._active_journey.roadmap
        is_on_roadmap = bool(roadmap.get_step_by_title(data["title"]))
        new_step = self._store.create_step(
            self._active_journey.id, title=data["title"],
            user_notes=data["notes"], suggestions=data["hints"])
        if not is_on_roadmap and roadmap.steps:
            roadmap.add_detour_step(data["title"], data["notes"],
                                    branch_from=self._current_step.step_number
                                    if self._current_step else None)
            self._store.update_roadmap(self._active_journey.id, roadmap)
            self._active_journey = self._store.get_journey(self._active_journey.id)
        self._steps = self._store.list_steps(self._active_journey.id)
        self._step_track.set_steps(self._steps)
        self._current_step = new_step; self._checklist_state = {}
        self._selected_rm_idx = idx_of_step(new_step, self._active_journey.roadmap)
        self._refresh_workspace(); self._refresh_sessions()
        self._refresh_overview(); self._refresh_journey_list()

    def _on_web_toggle(self, state: int):
        if self._active_journey:
            enabled = (state == Qt.CheckState.Checked.value)
            self._store.update_journey(self._active_journey.id,
                                       web_search_enabled=1 if enabled else 0)
            self._active_journey = self._store.get_journey(self._active_journey.id)

    def _on_step_track_clicked(self, idx: int):
        if idx < 0 or idx >= len(self._steps): return
        step = self._steps[idx]
        status_str = {
            "completed": f"\u2713 Completed"+(f" {step.completed_at[:10]}" if step.completed_at else ""),
            "active":    "\u2694 Current Step",
        }.get(step.status, step.status.capitalize())
        self._council_status.setText(f"Step {step.step_number}: {step.title}  \u2014  {status_str}")
        self._council_status.show()
        QTimer.singleShot(3500, self._council_status.hide)

    def _on_toggle_pause(self):
        if self._active_journey: self._on_toggle_pause_by_id(self._active_journey.id)

    def _on_toggle_pause_by_id(self, journey_id: str):
        journey = self._store.get_journey(journey_id)
        if not journey: return
        new_status = "active" if journey.status == "paused" else "paused"
        self._store.update_journey(journey_id, status=new_status)
        self._refresh_journey_list()
        if self._active_journey and self._active_journey.id == journey_id:
            self._active_journey = self._store.get_journey(journey_id)
            if self._active_journey:
                self._pause_btn.setText(
                    "\u25b6  Resume" if self._active_journey.status == "paused"
                    else "\u23f8  Pause")

    def _on_complete_journey(self):
        if not self._active_journey: return
        self._store.update_journey(self._active_journey.id, status="completed")
        self._refresh_journey_list()
        self._active_journey = self._store.get_journey(self._active_journey.id)
        self._pause_btn.setEnabled(False); self._complete_journey_btn.setEnabled(False)

    def _on_archive_journey(self, journey_id: str):
        self._store.update_journey(journey_id, status="archived")
        if self._active_journey and self._active_journey.id == journey_id:
            self._active_journey = None; self._right_stack.setCurrentIndex(0)
        self._refresh_journey_list()

    def _on_delete_journey(self, journey_id: str):
        reply = QMessageBox.question(
            self, "Delete Journey",
            "Permanently delete this journey and all its steps and council records?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        if reply != QMessageBox.StandardButton.Yes: return
        self._store.delete_journey(journey_id)
        if self._active_journey and self._active_journey.id == journey_id:
            self._active_journey = None; self._right_stack.setCurrentIndex(0)
        self._refresh_journey_list()

    def _on_complete_step(self):
        if not self._current_step: return
        self._flush_notes()
        # Pre-fill next step from roadmap
        next_rs = self._get_next_roadmap_steps(1)
        pft = next_rs[0].title if next_rs else ""
        pfn = ""
        if next_rs:
            rs  = next_rs[0]
            pfn = rs.description
            if rs.objectives:
                pfn += "\n\nObjectives:\n" + "\n".join(f"\u2022 {o}" for o in rs.objectives)
        dlg = AddStepDialog(self._palette, title="Define Next Step",
                            prefill_title=pft, prefill_notes=pfn, parent=self)
        if dlg.exec() != QDialog.DialogCode.Accepted: return
        data = dlg.get_data()
        self._store.complete_step(self._current_step.id)
        # Record detour if off-roadmap
        roadmap = self._active_journey.roadmap
        is_on_roadmap = bool(roadmap.get_step_by_title(data["title"]))
        new_step = self._store.create_step(
            self._active_journey.id, title=data["title"],
            user_notes=data["notes"], suggestions=data["hints"])
        if not is_on_roadmap and roadmap.steps:
            roadmap.add_detour_step(data["title"], data["notes"],
                                    branch_from=self._current_step.step_number)
            self._store.update_roadmap(self._active_journey.id, roadmap)
            self._active_journey = self._store.get_journey(self._active_journey.id)
        self._steps = self._store.list_steps(self._active_journey.id)
        self._step_track.set_steps(self._steps)
        self._current_step = new_step; self._checklist_state = {}
        self._selected_rm_idx = idx_of_step(new_step, self._active_journey.roadmap)
        self._refresh_workspace(); self._refresh_sessions()
        self._refresh_overview(); self._refresh_history(); self._refresh_journey_list()
        # Switch to Workspace — NO auto-convene, user decides when to convene
        self._tabs.setCurrentIndex(_TAB_WORKSPACE)

    def _on_convene_council(self):
        """Manual council convene — the only trigger for council calls."""
        if self._council_running: return
        self._flush_notes()
        if self._current_step:
            self._current_step = self._store.get_step(self._current_step.id)
        self._convene_council_async()

    def _on_update_roadmap(self):
        """Send current workspace notes+hints to LLM, update the roadmap."""
        if not self._active_journey: return
        notes = self._notes_edit.toPlainText().strip()
        hints = self._hints_edit.toPlainText().strip()
        pivot = "\n".join(filter(None, [notes, hints]))
        if not pivot:
            QMessageBox.information(self, "Update Roadmap",
                                    "Write notes or hints in the Workspace first, "
                                    "then click Update Roadmap to reshape the plan.")
            return
        llm_client = load_llm_client()
        if not llm_client:
            QMessageBox.warning(self, "No LLM",
                                "Configure API key in Network \u2192 LLM Settings.")
            return
        self._update_rm_btn.setEnabled(False)
        self._update_rm_btn.setText("\u23f3  Updating\u2026")
        self._council_status.setText("Updating roadmap\u2026"); self._council_status.show()
        journey = self._active_journey; steps = list(self._steps)

        def _worker():
            try:
                new_roadmap = _update_roadmap_from_pivot(llm_client, journey, steps, pivot)
                if new_roadmap.steps:
                    self._store.update_roadmap(journey.id, new_roadmap)
                QTimer.singleShot(0, self._on_roadmap_updated)
            except Exception as exc:
                err = str(exc)
                QTimer.singleShot(0, lambda e=err: self._on_roadmap_update_failed(e))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_roadmap_updated(self):
        self._update_rm_btn.setEnabled(True); self._update_rm_btn.setText("\U0001f504  Update Roadmap")
        self._council_status.hide()
        self._active_journey = self._store.get_journey(self._active_journey.id)
        if self._active_journey:
            self._selected_rm_idx = idx_of_step(self._current_step, self._active_journey.roadmap) \
                if self._current_step else -1
        self._refresh_overview(); self._refresh_journey_list()

    def _on_roadmap_update_failed(self, msg: str):
        self._update_rm_btn.setEnabled(True); self._update_rm_btn.setText("\U0001f504  Update Roadmap")
        self._council_status.hide()
        QMessageBox.warning(self, "Roadmap Update Failed", msg)

    def _on_regen_overview(self):
        if not self._current_step: return
        sessions = self._store.list_sessions_for_step(self._current_step.id)
        if not sessions: return
        latest     = sessions[-1]
        llm_client = load_llm_client()
        if not llm_client:
            QMessageBox.warning(self, "No LLM", "Configure API key in Network \u2192 LLM Settings.")
            return

        def _worker():
            try:
                cl, res, rm = _run_structured_call(
                    llm_client, latest.synthesis, self._active_journey, self._current_step)
                from src.data.database import get_connection as _gc
                c = _gc()
                c.execute(
                    "UPDATE journey_council_sessions SET "
                    "step_checklist=?,step_resources=?,roadmap_text=? WHERE id=?",
                    (json.dumps(cl), json.dumps(res), rm, latest.id))
                c.commit(); c.close()
                QTimer.singleShot(0, self._refresh_overview)
            except Exception as exc:
                QTimer.singleShot(0, lambda e=str(exc): QMessageBox.warning(
                    self, "Regen Error", e))
        threading.Thread(target=_worker, daemon=True).start()

    # ── Council execution ─────────────────────────────────────────────────────

    def _convene_council_async(self):
        if self._council_running: return
        if not self._current_step or not self._active_journey: return
        llm_client = load_llm_client()
        council    = load_council_config()
        if not llm_client:
            self._show_council_error(
                "No OpenRouter API key configured.\n"
                "Set it up in Network \u2192 LLM Settings."); return
        if not council:
            self._show_council_error(
                "Council not configured. Enable it in Network \u2192 Council Settings."); return

        self._council_running = True
        self._council_btn.setEnabled(False)
        self._council_btn.setText("\u23f3  Convening\u2026")
        self._council_status.show()
        self._council_status.setText("Starting council\u2026")

        journey = self._active_journey; steps = list(self._steps); step = self._current_step

        def _prog(msg: str):
            QTimer.singleShot(0, lambda m=msg: self._council_status.setText(m))

        def _worker():
            try:
                session = _run_council(
                    journey=journey, steps=steps, current_step=step,
                    llm_client=llm_client, council=council,
                    journey_store=self._store,
                    todo_store=self._todo_store, activity_store=self._activity_store,
                    calendar_store=self._calendar_store, on_progress=_prog)
                QTimer.singleShot(0, lambda s=session: self._on_council_done(s))
            except Exception as exc:
                err = str(exc)
                QTimer.singleShot(0, lambda e=err: self._show_council_error(e))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_council_done(self, session: CouncilSession):
        self._council_running = False
        self._council_btn.setEnabled(True)
        self._council_btn.setText("\u2694  Convene Council")
        self._council_status.hide()
        fresh = self._store.get_step(self._current_step.id)
        if fresh:
            self._current_step = fresh
            self._checklist_state = dict(fresh.checklist_state)
        self._refresh_sessions()
        self._refresh_overview()
        self._refresh_journey_list()
        # Switch to Overview to show results
        self._tabs.setCurrentIndex(_TAB_OVERVIEW)

    def _show_council_error(self, msg: str):
        self._council_running = False
        if hasattr(self, "_council_btn"):
            self._council_btn.setEnabled(True)
            self._council_btn.setText("\u2694  Convene Council")
        if hasattr(self, "_council_status"):
            self._council_status.hide()
        QMessageBox.warning(self, "Council Error", msg)

    def _refresh(self):
        self._refresh_journey_list()
        if self._active_journey:
            updated = self._store.get_journey(self._active_journey.id)
            if updated: self._active_journey = updated


# ── Module-level helper ───────────────────────────────────────────────────────

def idx_of_step(step: Optional[JourneyStep], roadmap: Roadmap) -> int:
    """Return the roadmap index matching the given step title, or -1."""
    if not step: return -1
    title_l = step.title.strip().lower()
    for i, rs in enumerate(roadmap.steps):
        if rs.title.strip().lower() == title_l:
            return i
    return -1