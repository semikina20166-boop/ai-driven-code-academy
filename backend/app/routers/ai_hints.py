from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import CurrentUser
from app.database import get_db
from app.models import Level, ProgressStatus, UserProgress
from app.schemas import AiHintRequest, AiHintResponse, CodeReviewRequest, CodeReviewResponse
from app.services.ai_service import get_hint, get_code_review

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/hint", response_model=AiHintResponse)
async def request_hint(body: AiHintRequest, user: CurrentUser, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Level).options(selectinload(Level.difficulty)).where(Level.id == body.level_id)
    )
    level = result.scalar_one_or_none()
    if not level:
        raise HTTPException(404, "Уровень не найден")

    prog = await db.get(UserProgress, {"user_id": user.id, "level_id": level.id})
    if not prog or prog.status == ProgressStatus.locked:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Уровень недоступен")

    # Enforce hint limit for Free users (max 3 hints per calendar day)
    if not user.is_premium:
        today = date.today()
        if user.last_hint_date == today:
            if user.hints_used_today >= 3:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Исчерпан дневной лимит бесплатных подсказок (3 в день). Активируйте Premium для безлимитного ИИ-наставника."
                )
            user.hints_used_today += 1
        else:
            user.last_hint_date = today
            user.hints_used_today = 1
        await db.commit()

    hint = await get_hint(
        task_text=level.task_text,
        user_code=body.code,
        error_message=body.error_message,
        difficulty_name=level.difficulty.name_ru,
        level_title=level.title,
        allowed_concepts=list(level.allowed_concepts or []),
    )
    return AiHintResponse(hint=hint)


@router.post("/review", response_model=CodeReviewResponse)
async def request_review(body: CodeReviewRequest, user: CurrentUser, db: AsyncSession = Depends(get_db)):
    if not user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="ИИ-обзор решения доступен только для пользователей с Premium-подпиской."
        )

    result = await db.execute(
        select(Level).options(selectinload(Level.difficulty)).where(Level.id == body.level_id)
    )
    level = result.scalar_one_or_none()
    if not level:
        raise HTTPException(404, "Уровень не найден")

    prog = await db.get(UserProgress, {"user_id": user.id, "level_id": level.id})
    if not prog or prog.status != ProgressStatus.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ИИ-обзор кода доступен только после успешного прохождения уровня."
        )

    review = await get_code_review(
        task_text=level.task_text,
        user_code=body.code,
        difficulty_name=level.difficulty.name_ru,
        level_title=level.title,
    )
    return CodeReviewResponse(review=review)
