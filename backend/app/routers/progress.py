from fastapi import APIRouter, Depends

from app.auth import CurrentUser
from app.database import get_db
from app.schemas import ProgressSummary
from app.services.progress_service import progress_summary
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/summary", response_model=ProgressSummary)
async def get_summary(user: CurrentUser, db: AsyncSession = Depends(get_db)):
    data = await progress_summary(db, user.id)
    return ProgressSummary(**data)
