from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class SourceTypeEnum(str, Enum):
    CORPUS = "corpus"
    WEB = "web"
    ALL = "all"

class RecencyWindowEnum(str, Enum):
    ONE_YEAR = "1y"
    THREE_YEARS = "3y"
    FIVE_YEARS = "5y"
    ANY = "any"

class SearchInformationArgs(BaseModel):
    query: str = Field(..., min_length=2, max_length=200, description="Search query string")
    source_type: SourceTypeEnum = Field(default=SourceTypeEnum.CORPUS)
    max_results: int = Field(default=5, ge=1, le=20, description="Max results to return (bounded)")
    recency_window: Optional[RecencyWindowEnum] = Field(default=RecencyWindowEnum.ANY)

class RetrieveDocumentArgs(BaseModel):
    document_id: str = Field(..., description="Unique document ID present in the index")
    section: Optional[str] = Field(None, description="Optional section identifier")

class CalculateMetricArgs(str, Enum):
    GROWTH_RATE = "growth_rate"
    CAGR = "cagr"
    SHARE = "share"
    RATIO = "ratio"
    AVERAGE = "average"