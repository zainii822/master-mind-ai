from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ClaimType(str, Enum):
    FACT = "fact"
    INFERENCE = "inference"
    RECOMMENDATION = "recommendation"
    UNCERTAINTY = "uncertainty"

class SourceKind(str, Enum):
    RETRIEVED_DOCUMENT = "retrieved_document"
    SEARCH_RESULT = "search_result"
    CALCULATION = "calculation"
    MODEL_GENERATED = "model_generated"

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"

class EvidenceRecord(BaseModel):
    evidence_id: str = Field(..., description="Stable unique identifier for the evidence record")
    question_id: str = Field(..., description="Which sub-question this was gathered for")
    claim: str = Field(..., description="The specific statement being supported")
    claim_type: ClaimType
    source_ref: str = Field(..., description="ID of the tool result this came from (must resolve)")
    source_kind: SourceKind
    source_detail: str = Field(..., description="Title, identifier, or date where available")
    credibility: ConfidenceLevel
    recency: str = Field(..., description="Date or timeframe bucket")
    corroboration: List[str] = Field(default_factory=list, description="List of other evidence IDs supporting the same claim")
    confidence: ConfidenceLevel
    analyst_notes: Optional[str] = Field(None, description="Why accepted or why flagged")