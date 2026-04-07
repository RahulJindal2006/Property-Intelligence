from fastapi import APIRouter, Header, HTTPException
from app.models.issues import IssueCreate
from app.services.issue_service import save_issue, get_all_issues, resolve_issue

router = APIRouter(prefix="/api", tags=["issues"])


@router.post("/issues")
async def create_issue(issue: IssueCreate):
    success = save_issue(issue)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save issue")
    return {"status": "success"}


@router.get("/issues")
async def list_issues(x_admin_password: str = Header()):
    result = get_all_issues(x_admin_password)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid password")
    return result


@router.post("/issues/{issue_id}/resolve")
async def mark_resolved(issue_id: int, x_admin_password: str = Header()):
    success = resolve_issue(issue_id, x_admin_password)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to resolve issue")
    return {"status": "resolved"}
