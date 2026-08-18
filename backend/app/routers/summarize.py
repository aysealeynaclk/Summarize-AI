from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.groq_client import summarize_text
from app.models import AILog, User
from app.schemas import LogOut, SummarizeRequest, SummarizeResponse

router = APIRouter(tags=["summarize"])


@router.post("/summarize", response_model=SummarizeResponse)
def summarize(
    payload: SummarizeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    summary = summarize_text(payload.text, payload.language)

    log = AILog(
        user_id=current_user.id,
        input_text=payload.text,
        output_summary=summary,
        provider="groq",
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return SummarizeResponse(summary=summary, created_at=log.created_at)


@router.get("/summaries/me", response_model=list[LogOut])
def my_summaries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logs = (
        db.query(AILog)
        .filter(AILog.user_id == current_user.id)
        .order_by(AILog.created_at.desc())
        .limit(3)
        .all()
    )
    return logs
