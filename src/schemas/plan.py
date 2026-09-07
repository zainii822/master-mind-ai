from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class EvidenceType(str, Enum):
    FACT = "fact"
    INFERENCE = "inference"
    RECOMMENDATION = "recommendation"
    UNCERTAINTY = "uncertainty"

class CandidateTool(str, Enum):
    SEARCH_INFORMATION = "search_information"
    RETRIEVE_DOCUMENT = "retrieve_document"
    CALCULATE_METRIC = "calculate_metric"
    COMPARE_COMPANIES = "compare_companies"

class SubQuestion(BaseModel):
    id: str = Field(..., description="Unique sub-question ID, e.g., Q1.1")
    text: str = Field(..., description="Specific answerable sub-question")
    required_evidence_type: EvidenceType
    candidate_tools: List[CandidateTool]

class ResearchObjective(BaseModel):
    objective_id: str = Field(..., description="Objective identifier, e.g., Obj-1")
    title: str = Field(..., description="Strategic objective title")
    sub_questions: List[SubQuestion] = Field(..., min_length=2, max_length=5)

class ResearchPlan(BaseModel):
    objectives: List[ResearchObjective] = Field(..., min_length=3, max_length=6)
    assumptions: List[str] = Field(default_factory=list, description="Explicitly defaulted assumptions made during planning")