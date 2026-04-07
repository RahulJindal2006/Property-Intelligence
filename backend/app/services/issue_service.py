import os
import pandas as pd
from datetime import datetime
from app.config import ISSUES_FILE, RESOLVED_ISSUES_FILE
from app.models.issues import IssueCreate, IssueResponse, IssuesListResponse


def save_issue(issue: IssueCreate) -> bool:
    try:
        new_issue = pd.DataFrame([{
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Question': issue.question,
            'What_Went_Wrong': issue.what_went_wrong,
            'Severity': issue.severity
        }])
        if os.path.exists(ISSUES_FILE):
            existing = pd.read_csv(ISSUES_FILE)
            updated = pd.concat([existing, new_issue], ignore_index=True)
        else:
            updated = new_issue
        updated.to_csv(ISSUES_FILE, index=False)
        return True
    except Exception:
        return False


def get_all_issues(password: str) -> IssuesListResponse | None:
    from app.config import ADMIN_PASSWORD
    if password != ADMIN_PASSWORD:
        return None

    if not os.path.exists(ISSUES_FILE):
        return IssuesListResponse(
            open_issues=[], resolved_issues=[],
            total=0, open_count=0, high_count=0, medium_count=0, low_count=0
        )

    df_raw = pd.read_csv(ISSUES_FILE)
    df_raw['Timestamp'] = pd.to_datetime(df_raw['Timestamp'])

    if os.path.exists(RESOLVED_ISSUES_FILE):
        df_resolved = pd.read_csv(RESOLVED_ISSUES_FILE)
        df_resolved['Timestamp'] = pd.to_datetime(df_resolved['Timestamp'])
    else:
        df_resolved = pd.DataFrame(columns=['Timestamp', 'Question', 'What_Went_Wrong', 'Severity', 'Resolved_At'])

    if not df_resolved.empty and 'Question' in df_resolved.columns:
        resolved_keys = set(
            zip(df_resolved['Timestamp'].astype(str), df_resolved['Question'])
        )
        df_open = df_raw[
            ~df_raw.apply(lambda r: (str(r['Timestamp']), r['Question']) in resolved_keys, axis=1)
        ].copy()
    else:
        df_open = df_raw.copy()

    open_issues = []
    for i, row in df_open.iterrows():
        open_issues.append(IssueResponse(
            id=int(i),
            timestamp=str(row['Timestamp']),
            question=str(row['Question']),
            what_went_wrong=str(row['What_Went_Wrong']),
            severity=str(row.get('Severity', 'Low'))
        ))

    resolved_issues = []
    for i, row in df_resolved.iterrows():
        resolved_issues.append(IssueResponse(
            id=int(i),
            timestamp=str(row['Timestamp']),
            question=str(row['Question']),
            what_went_wrong=str(row['What_Went_Wrong']),
            severity=str(row.get('Severity', 'Low')),
            resolved_at=str(row.get('Resolved_At', ''))
        ))

    return IssuesListResponse(
        open_issues=open_issues,
        resolved_issues=resolved_issues,
        total=len(df_raw),
        open_count=len(df_open),
        high_count=len(df_open[df_open['Severity'] == 'High']),
        medium_count=len(df_open[df_open['Severity'] == 'Medium']),
        low_count=len(df_open[df_open['Severity'] == 'Low'])
    )


def resolve_issue(issue_id: int, password: str) -> bool:
    from app.config import ADMIN_PASSWORD
    if password != ADMIN_PASSWORD:
        return False

    if not os.path.exists(ISSUES_FILE):
        return False

    df_raw = pd.read_csv(ISSUES_FILE)
    if issue_id < 0 or issue_id >= len(df_raw):
        return False

    row = df_raw.iloc[issue_id]
    resolved_row = pd.DataFrame([{
        'Timestamp': row['Timestamp'],
        'Question': row['Question'],
        'What_Went_Wrong': row['What_Went_Wrong'],
        'Severity': row['Severity'],
        'Resolved_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    if os.path.exists(RESOLVED_ISSUES_FILE):
        existing = pd.read_csv(RESOLVED_ISSUES_FILE)
        pd.concat([existing, resolved_row], ignore_index=True).to_csv(RESOLVED_ISSUES_FILE, index=False)
    else:
        resolved_row.to_csv(RESOLVED_ISSUES_FILE, index=False)

    return True
