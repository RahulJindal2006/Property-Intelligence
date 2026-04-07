from pydantic import BaseModel
from typing import Optional


class IssueCreate(BaseModel):
    question: str
    what_went_wrong: str
    severity: str = "Low"


class IssueResponse(BaseModel):
    id: int
    timestamp: str
    question: str
    what_went_wrong: str
    severity: str
    resolved_at: Optional[str] = None


class IssuesListResponse(BaseModel):
    open_issues: list[IssueResponse]
    resolved_issues: list[IssueResponse]
    total: int
    open_count: int
    high_count: int
    medium_count: int
    low_count: int
