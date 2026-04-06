"""Journey store — CRUD for journeys, steps, and council session records."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from typing import Optional

from src.data.database import get_connection
from src.utils.timestamps import now_utc

JOURNEY_DOMAINS = [
    "Coding", "Language Learning", "Creative",
    "Business / Freelance", "Health & Fitness", "Academic", "General",
]

DOMAIN_COLORS = {
    "Coding":              "#89b4fa",
    "Language Learning":   "#a6e3a1",
    "Creative":            "#f5c2e7",
    "Business / Freelance":"#fab387",
    "Health & Fitness":    "#94e2d5",
    "Academic":            "#cba6f7",
    "General":             "#89dceb",
}


@dataclass
class RoadmapStep:
    number:      int
    title:       str
    description: str
    objectives:  list[str] = field(default_factory=list)
    is_detour:   bool      = False   # True = step not in original plan
    branch_from: Optional[int] = None  # parent step number for detours


@dataclass
class Roadmap:
    overview: str
    steps:    list[RoadmapStep] = field(default_factory=list)

    @classmethod
    def from_json(cls, raw: str) -> "Roadmap":
        try:
            data = json.loads(raw or "{}")
            steps = [
                RoadmapStep(
                    number=s.get("number", i + 1),
                    title=s.get("title", ""),
                    description=s.get("description", ""),
                    objectives=s.get("objectives", []),
                    is_detour=bool(s.get("is_detour", False)),
                    branch_from=s.get("branch_from"),
                )
                for i, s in enumerate(data.get("steps", []))
            ]
            return cls(overview=data.get("overview", ""), steps=steps)
        except Exception:
            return cls(overview="")

    def to_json(self) -> str:
        return json.dumps({
            "overview": self.overview,
            "steps": [
                {
                    "number":      s.number,
                    "title":       s.title,
                    "description": s.description,
                    "objectives":  s.objectives,
                    "is_detour":   s.is_detour,
                    "branch_from": s.branch_from,
                }
                for s in self.steps
            ],
        })

    def add_detour_step(self, title: str, description: str,
                        branch_from: Optional[int] = None) -> RoadmapStep:
        """Append a detour step to the roadmap and return it."""
        next_num = (max(s.number for s in self.steps) + 1) if self.steps else 1
        rs = RoadmapStep(
            number=next_num, title=title, description=description,
            is_detour=True, branch_from=branch_from,
        )
        self.steps.append(rs)
        return rs

    def get_step_by_title(self, title: str) -> Optional[RoadmapStep]:
        t = title.strip().lower()
        for s in self.steps:
            if s.title.strip().lower() == t:
                return s
        return None


@dataclass
class Journey:
    id:                 str
    title:              str
    goal_description:   str
    domain:             str
    status:             str
    web_search_enabled: bool
    created_at:         str
    updated_at:         str
    step_count:         int = 0
    completed_steps:    int = 0
    roadmap_json:       str = ""

    @property
    def roadmap(self) -> Roadmap:
        return Roadmap.from_json(self.roadmap_json)

    @property
    def progress_pct(self) -> float:
        return self.completed_steps / self.step_count if self.step_count else 0.0

    @property
    def domain_color(self) -> str:
        return DOMAIN_COLORS.get(self.domain, "#89dceb")


@dataclass
class JourneyStep:
    id:                    str
    journey_id:            str
    step_number:           int
    title:                 str
    user_notes:            str
    user_next_suggestions: str
    status:                str
    created_at:            str
    completed_at:          Optional[str]
    checklist_state:       dict = field(default_factory=dict)
    council_sessions:      list["CouncilSession"] = field(default_factory=list)


@dataclass
class CouncilSession:
    id:                 str
    step_id:            str
    synthesis:          str
    synthesis_model:    str
    synthesis_mode:     str
    web_search_used:    bool
    web_search_queries: list[str]
    created_at:         str
    step_checklist:     list[str] = field(default_factory=list)
    step_resources:     list[str] = field(default_factory=list)
    roadmap_text:       str       = ""
    member_records:     list["CouncilMemberRecord"] = field(default_factory=list)


@dataclass
class CouncilMemberRecord:
    id:               str
    session_id:       str
    councilor_label:  str
    model:            str
    raw_response:     str
    created_at:       str


class JourneyStore:

    # ── Journeys ──────────────────────────────────────────────────────────────

    def create_journey(self, title: str, goal: str, domain: str,
                       web_search: bool = False) -> Journey:
        """Create a new journey. Only defined ONCE — no duplicate."""
        conn = get_connection()
        jid  = str(uuid.uuid4())
        now  = now_utc()
        conn.execute(
            "INSERT INTO journeys "
            "(id,title,goal_description,domain,status,"
            "web_search_enabled,created_at,updated_at,roadmap_json) "
            "VALUES (?,?,?,?,'active',?,?,?,'')",
            (jid, title.strip(), goal.strip(), domain,
             1 if web_search else 0, now, now),
        )
        conn.commit()
        conn.close()
        return Journey(
            id=jid, title=title.strip(), goal_description=goal.strip(),
            domain=domain, status="active", web_search_enabled=web_search,
            created_at=now, updated_at=now,
        )

    def list_journeys(self, include_archived: bool = False) -> list[Journey]:
        conn = get_connection()
        sf = "" if include_archived else "AND j.status != 'archived'"
        rows = conn.execute(
            f"SELECT j.*,"
            f"(SELECT COUNT(*) FROM journey_steps s WHERE s.journey_id=j.id) AS step_count,"
            f"(SELECT COUNT(*) FROM journey_steps s WHERE s.journey_id=j.id"
            f" AND s.status='completed') AS completed_steps "
            f"FROM journeys j WHERE j.deleted=0 {sf} ORDER BY j.updated_at DESC"
        ).fetchall()
        conn.close()
        return [self._row_to_journey(r) for r in rows]

    def get_journey(self, journey_id: str) -> Optional[Journey]:
        conn = get_connection()
        row = conn.execute(
            "SELECT j.*,"
            "(SELECT COUNT(*) FROM journey_steps s WHERE s.journey_id=j.id) AS step_count,"
            "(SELECT COUNT(*) FROM journey_steps s WHERE s.journey_id=j.id"
            " AND s.status='completed') AS completed_steps "
            "FROM journeys j WHERE j.id=?", (journey_id,)
        ).fetchone()
        conn.close()
        return self._row_to_journey(row) if row else None

    def update_journey(self, journey_id: str, **kwargs) -> None:
        allowed = {"title", "goal_description", "domain", "status",
                   "web_search_enabled", "roadmap_json"}
        fields  = {k: v for k, v in kwargs.items() if k in allowed}
        if not fields:
            return
        fields["updated_at"] = now_utc()
        setters = ", ".join(f"{k}=?" for k in fields)
        conn = get_connection()
        conn.execute(f"UPDATE journeys SET {setters} WHERE id=?",
                     (*fields.values(), journey_id))
        conn.commit()
        conn.close()

    def update_roadmap(self, journey_id: str, roadmap: Roadmap) -> None:
        """Convenience wrapper to persist an updated Roadmap object."""
        self.update_journey(journey_id, roadmap_json=roadmap.to_json())

    def delete_journey(self, journey_id: str) -> None:
        conn = get_connection()
        conn.execute(
            "UPDATE journeys SET deleted=1, updated_at=? WHERE id=?",
            (now_utc(), journey_id))
        conn.commit()
        conn.close()

    # ── Steps ─────────────────────────────────────────────────────────────────

    def create_step(self, journey_id: str, title: str,
                    user_notes: str = "", suggestions: str = "") -> JourneyStep:
        conn = get_connection()
        row = conn.execute(
            "SELECT MAX(step_number) FROM journey_steps WHERE journey_id=?",
            (journey_id,)).fetchone()
        next_num = (row[0] or 0) + 1
        sid = str(uuid.uuid4())
        now = now_utc()
        conn.execute(
            "INSERT INTO journey_steps "
            "(id,journey_id,step_number,title,user_notes,"
            "user_next_suggestions,status,created_at) "
            "VALUES (?,?,?,?,?,?,'active',?)",
            (sid, journey_id, next_num, title.strip(), user_notes, suggestions, now),
        )
        conn.execute("UPDATE journeys SET updated_at=? WHERE id=?", (now, journey_id))
        conn.commit()
        conn.close()
        return JourneyStep(
            id=sid, journey_id=journey_id, step_number=next_num,
            title=title.strip(), user_notes=user_notes,
            user_next_suggestions=suggestions, status="active",
            created_at=now, completed_at=None,
        )

    def list_steps(self, journey_id: str) -> list[JourneyStep]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM journey_steps WHERE journey_id=? ORDER BY step_number ASC",
            (journey_id,)).fetchall()
        conn.close()
        return [self._row_to_step(r) for r in rows]

    def get_step(self, step_id: str) -> Optional[JourneyStep]:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM journey_steps WHERE id=?", (step_id,)).fetchone()
        conn.close()
        return self._row_to_step(row) if row else None

    def update_step_notes(self, step_id: str, user_notes: str,
                          suggestions: str) -> None:
        conn = get_connection()
        conn.execute(
            "UPDATE journey_steps SET user_notes=?, user_next_suggestions=? WHERE id=?",
            (user_notes, suggestions, step_id))
        conn.commit()
        conn.close()

    def update_checklist_state(self, step_id: str, state: dict) -> None:
        conn = get_connection()
        conn.execute(
            "UPDATE journey_steps SET checklist_state=? WHERE id=?",
            (json.dumps(state), step_id))
        conn.commit()
        conn.close()

    def complete_step(self, step_id: str) -> None:
        conn = get_connection()
        conn.execute(
            "UPDATE journey_steps SET status='completed', completed_at=? WHERE id=?",
            (now_utc(), step_id))
        conn.commit()
        conn.close()

    # ── Council Sessions ──────────────────────────────────────────────────────

    def save_council_session(
        self, step_id: str, synthesis: str, synthesis_model: str,
        synthesis_mode: str, web_search_used: bool, web_search_queries: list[str],
        member_records: list[dict],
        step_checklist: list[str] = None, step_resources: list[str] = None,
        roadmap_text: str = "",
    ) -> CouncilSession:
        conn    = get_connection()
        sess_id = str(uuid.uuid4())
        now     = now_utc()
        conn.execute(
            "INSERT INTO journey_council_sessions "
            "(id,step_id,synthesis,synthesis_model,synthesis_mode,"
            "web_search_used,web_search_queries,created_at,"
            "step_checklist,step_resources,roadmap_text) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (sess_id, step_id, synthesis, synthesis_model, synthesis_mode,
             1 if web_search_used else 0, json.dumps(web_search_queries), now,
             json.dumps(step_checklist or []),
             json.dumps(step_resources or []),
             roadmap_text),
        )
        members: list[CouncilMemberRecord] = []
        for rec in member_records:
            mid = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO journey_council_members "
                "(id,session_id,councilor_label,model,raw_response,created_at) "
                "VALUES (?,?,?,?,?,?)",
                (mid, sess_id,
                 rec.get("label", rec.get("model", "")).split("/")[-1][:20],
                 rec["model"], rec["response"], now),
            )
            members.append(CouncilMemberRecord(
                id=mid, session_id=sess_id,
                councilor_label=rec.get("label", rec.get("model", "")).split("/")[-1][:20],
                model=rec["model"], raw_response=rec["response"], created_at=now,
            ))
        conn.commit()
        conn.close()
        return CouncilSession(
            id=sess_id, step_id=step_id, synthesis=synthesis,
            synthesis_model=synthesis_model, synthesis_mode=synthesis_mode,
            web_search_used=web_search_used, web_search_queries=web_search_queries,
            created_at=now,
            step_checklist=step_checklist or [],
            step_resources=step_resources or [],
            roadmap_text=roadmap_text,
            member_records=members,
        )

    def list_sessions_for_step(self, step_id: str) -> list[CouncilSession]:
        conn      = get_connection()
        sess_rows = conn.execute(
            "SELECT * FROM journey_council_sessions "
            "WHERE step_id=? ORDER BY created_at ASC", (step_id,)).fetchall()

        def _jl(val, default):
            try:
                r = json.loads(val or "null")
                return r if r is not None else default
            except Exception:
                return default

        sessions = []
        for s in sess_rows:
            sk = s.keys()
            mem_rows = conn.execute(
                "SELECT * FROM journey_council_members "
                "WHERE session_id=? ORDER BY rowid ASC", (s["id"],)).fetchall()
            members = [
                CouncilMemberRecord(
                    id=m["id"], session_id=m["session_id"],
                    councilor_label=m["councilor_label"], model=m["model"],
                    raw_response=m["raw_response"], created_at=m["created_at"],
                )
                for m in mem_rows
            ]
            sessions.append(CouncilSession(
                id=s["id"], step_id=s["step_id"],
                synthesis=s["synthesis"] or "",
                synthesis_model=s["synthesis_model"],
                synthesis_mode=s["synthesis_mode"],
                web_search_used=bool(s["web_search_used"]),
                web_search_queries=_jl(s["web_search_queries"], []),
                created_at=s["created_at"],
                step_checklist=_jl(s["step_checklist"] if "step_checklist" in sk else None, []),
                step_resources=_jl(s["step_resources"]  if "step_resources"  in sk else None, []),
                roadmap_text=(s["roadmap_text"] if "roadmap_text" in sk else "") or "",
                member_records=members,
            ))
        conn.close()
        return sessions

    # ── Private helpers ───────────────────────────────────────────────────────

    def _row_to_journey(self, row) -> Journey:
        keys = row.keys()
        return Journey(
            id=row["id"], title=row["title"],
            goal_description=row["goal_description"],
            domain=row["domain"], status=row["status"],
            web_search_enabled=bool(row["web_search_enabled"]),
            created_at=row["created_at"], updated_at=row["updated_at"],
            step_count=(row["step_count"] if "step_count" in keys else 0),
            completed_steps=(row["completed_steps"] if "completed_steps" in keys else 0),
            roadmap_json=(row["roadmap_json"] if "roadmap_json" in keys else "") or "",
        )

    def _row_to_step(self, row) -> JourneyStep:
        keys = row.keys()
        raw  = (row["checklist_state"] if "checklist_state" in keys else None) or "{}"
        try:
            cs = json.loads(raw)
            if not isinstance(cs, dict):
                cs = {}
        except Exception:
            cs = {}
        return JourneyStep(
            id=row["id"], journey_id=row["journey_id"],
            step_number=row["step_number"], title=row["title"],
            user_notes=row["user_notes"] or "",
            user_next_suggestions=row["user_next_suggestions"] or "",
            status=row["status"], created_at=row["created_at"],
            completed_at=row["completed_at"] if row["completed_at"] else None,
            checklist_state=cs,
        )