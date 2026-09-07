from typing import List, Dict, Any
from pydantic import BaseModel, Field
from src.schemas.plan import ResearchPlan
from src.schemas.evidence import EvidenceRecord

class ResearchState(BaseModel):
    run_id: str
    scope_description: str
    plan: ResearchPlan
    question_status: Dict[str, str] = Field(default_factory=dict) # q_id -> "open" | "answered" | "unanswerable"
    evidence_store: List[EvidenceRecord] = Field(default_factory=list)
    tool_history: List[Dict[str, Any]] = Field(default_factory=list)
    iteration_count: int = 0
    cumulative_tokens_in: int = 0
    cumulative_tokens_out: int = 0
    estimated_cost_usd: float = 0.0
    defect_list: List[Dict[str, Any]] = Field(default_factory=list)
    current_stage: str = "intake"

    def initialize_statuses(self):
        for obj in self.plan.objectives:
            for sq in obj.sub_questions:
                self.question_status[sq.id] = "open"

    def get_next_open_question(self) -> tuple[str, str] | None:
        """Returns (objective_id, sub_question_text) for the next open question."""
        for obj in self.plan.objectives:
            for sq in obj.sub_questions:
                if self.question_status.get(sq.id) == "open":
                    return sq.id, sq.text
        return None

    def mark_question_resolved(self, question_id: str, status: str = "answered"):
        self.question_status[question_id] = status