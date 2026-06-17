from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import CurrentUser
from app.database import get_db
from app.models import Difficulty, Level, ProgressStatus, UserProgress
from app.schemas import LevelDetailOut, LevelMapItem, RunCodeRequest, RunCodeResponse
from app.services.code_runner import run_tests_for_language
from app.services.progress_service import (
    ensure_first_level_open,
    get_progress_map,
    mark_level_completed,
    reconcile_track_unlocks,
)

router = APIRouter(prefix="/levels", tags=["levels"])


def _pick(ru: str, en: str, kz: str, lang: str) -> str:
    """Return the field for the requested language, falling back to Russian."""
    m = {"ru": ru or "", "en": en or ru or "", "kz": kz or ru or ""}
    return m.get(lang, ru or "")


@router.get("/track/{track_id}/map", response_model=list[LevelMapItem])
async def level_map(
    track_id: int,
    user: CurrentUser,
    lang: str = Query(default="ru", regex="^(ru|en|kz)$"),
    db: AsyncSession = Depends(get_db),
):
    await ensure_first_level_open(db, user.id, track_id)
    await reconcile_track_unlocks(db, user.id, track_id)
    await db.commit()

    result = await db.execute(
        select(Level, Difficulty)
        .join(Difficulty, Difficulty.id == Level.difficulty_id)
        .where(Level.track_id == track_id)
        .order_by(Difficulty.sort_order, Level.order_num)
    )
    prog = await get_progress_map(db, user.id)

    items: list[LevelMapItem] = []
    for level, diff in result.all():
        status_val = prog.get(level.id, ProgressStatus.locked)
        title_ru = level.title_ru or ""
        title_en = level.title_en or title_ru
        title_kz = level.title_kz or title_ru
        diff_ru = diff.name_ru or ""
        diff_en = getattr(diff, "name_en", "") or diff_ru
        diff_kz = getattr(diff, "name_kz", "") or diff_ru
        items.append(
            LevelMapItem(
                id=level.id,
                order_num=level.order_num,
                title=_pick(title_ru, title_en, title_kz, lang),
                title_ru=title_ru,
                title_en=title_en,
                title_kz=title_kz,
                difficulty_code=diff.code,
                difficulty_name=_pick(diff_ru, diff_en, diff_kz, lang),
                difficulty_name_ru=diff_ru,
                difficulty_name_en=diff_en,
                difficulty_name_kz=diff_kz,
                status=status_val.value if isinstance(status_val, ProgressStatus) else str(status_val),
            )
        )
    return items


@router.get("/{level_id}", response_model=LevelDetailOut)
async def get_level(
    level_id: int,
    user: CurrentUser,
    lang: str = Query(default="ru", regex="^(ru|en|kz)$"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Level)
        .options(selectinload(Level.difficulty))
        .where(Level.id == level_id)
    )
    level = result.scalar_one_or_none()
    if not level:
        raise HTTPException(404, "Уровень не найден")

    # Enforce premium check on Hard levels
    if level.difficulty.code == "hard" and not user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Для доступа к сложным уровням требуется Premium-подписка."
        )

    prog = await db.get(UserProgress, {"user_id": user.id, "level_id": level_id})
    status_val = prog.status.value if prog else ProgressStatus.locked.value

    if status_val == ProgressStatus.locked.value:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Уровень заблокирован")

    diff = level.difficulty
    title_ru = level.title_ru or ""
    title_en = level.title_en or title_ru
    title_kz = level.title_kz or title_ru
    task_ru = level.task_text_ru or ""
    task_en = level.task_text_en or task_ru
    task_kz = level.task_text_kz or task_ru
    theory_ru = level.theory_ru
    theory_en = level.theory_en or theory_ru
    theory_kz = level.theory_kz or theory_ru
    diff_ru = diff.name_ru or ""
    diff_en = getattr(diff, "name_en", "") or diff_ru
    diff_kz = getattr(diff, "name_kz", "") or diff_ru

    return LevelDetailOut(
        id=level.id,
        track_id=level.track_id,
        order_num=level.order_num,
        title=_pick(title_ru, title_en, title_kz, lang),
        title_ru=title_ru,
        title_en=title_en,
        title_kz=title_kz,
        task_text=_pick(task_ru, task_en, task_kz, lang),
        task_text_ru=task_ru,
        task_text_en=task_en,
        task_text_kz=task_kz,
        starter_code=level.starter_code,
        status=status_val,
        allowed_concepts=list(level.allowed_concepts or []),
        difficulty_code=diff.code,
        difficulty_name=_pick(diff_ru, diff_en, diff_kz, lang),
        difficulty_name_ru=diff_ru,
        difficulty_name_en=diff_en,
        difficulty_name_kz=diff_kz,
        theory=_pick(theory_ru or "", theory_en or "", theory_kz or "", lang) or None,
        theory_ru=theory_ru,
        theory_en=theory_en,
        theory_kz=theory_kz,
    )


@router.post("/run", response_model=RunCodeResponse)
async def run_level(body: RunCodeRequest, user: CurrentUser, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Level).options(selectinload(Level.difficulty)).where(Level.id == body.level_id)
    )
    level = result.scalar_one_or_none()
    if not level:
        raise HTTPException(404, "Уровень не найден")

    prog = await db.get(UserProgress, {"user_id": user.id, "level_id": level.id})
    if not prog or prog.status == ProgressStatus.locked:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Уровень недоступен")

    if prog.status == ProgressStatus.open:
        prog.attempts += 1

    test_result = run_tests_for_language(body.code, level.solution_tests)

    if test_result["passed"]:
        await mark_level_completed(db, user.id, level)

    await db.commit()
    return RunCodeResponse(**test_result)
