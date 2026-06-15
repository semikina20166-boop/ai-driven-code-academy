from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Difficulty, Language, Level, ProgressStatus, Track, UserProgress


async def get_progress_map(db: AsyncSession, user_id: UUID) -> dict[int, ProgressStatus]:
    result = await db.execute(select(UserProgress).where(UserProgress.user_id == user_id))
    return {row.level_id: row.status for row in result.scalars().all()}


async def ensure_first_level_open(db: AsyncSession, user_id: UUID, track_id: int) -> None:
    """First level (easy, order 1) is open when user opens a track."""
    q = await db.execute(
        select(Level)
        .join(Difficulty, Difficulty.id == Level.difficulty_id)
        .where(Level.track_id == track_id, Difficulty.code == "easy", Level.order_num == 1)
    )
    first = q.scalar_one_or_none()
    if not first:
        return

    existing = await db.get(UserProgress, {"user_id": user_id, "level_id": first.id})
    if existing:
        if existing.status == ProgressStatus.locked:
            existing.status = ProgressStatus.open
        return

    db.add(
        UserProgress(
            user_id=user_id,
            level_id=first.id,
            status=ProgressStatus.open,
            attempts=0,
        )
    )


async def unlock_next_level(
    db: AsyncSession,
    user_id: UUID,
    level: Level,
) -> None:
    nq = await db.execute(
        select(Level).where(
            Level.track_id == level.track_id,
            Level.difficulty_id == level.difficulty_id,
            Level.order_num == level.order_num + 1,
        )
    )
    nxt = nq.scalar_one_or_none()
    if not nxt:
        return

    np = await db.get(UserProgress, {"user_id": user_id, "level_id": nxt.id})
    if not np:
        db.add(UserProgress(user_id=user_id, level_id=nxt.id, status=ProgressStatus.open, attempts=0))
    elif np.status == ProgressStatus.locked:
        np.status = ProgressStatus.open


async def mark_level_completed(
    db: AsyncSession,
    user_id: UUID,
    level: Level,
) -> None:
    prog = await db.get(UserProgress, {"user_id": user_id, "level_id": level.id})
    if not prog:
        prog = UserProgress(user_id=user_id, level_id=level.id, status=ProgressStatus.open, attempts=0)
        db.add(prog)

    prog.status = ProgressStatus.completed
    prog.completed_at = datetime.now(timezone.utc)
    await unlock_next_level(db, user_id, level)


async def count_completed_in_block(
    db: AsyncSession,
    user_id: UUID,
    track_id: int,
    difficulty_id: int,
) -> tuple[int, int]:
    total_q = await db.execute(
        select(func.count())
        .select_from(Level)
        .where(Level.track_id == track_id, Level.difficulty_id == difficulty_id)
    )
    total = total_q.scalar() or 0

    done_q = await db.execute(
        select(func.count())
        .select_from(UserProgress)
        .join(Level, Level.id == UserProgress.level_id)
        .where(
            UserProgress.user_id == user_id,
            UserProgress.status == ProgressStatus.completed,
            Level.track_id == track_id,
            Level.difficulty_id == difficulty_id,
        )
    )
    done = done_q.scalar() or 0
    return done, total


async def progress_summary(db: AsyncSession, user_id: UUID) -> dict:
    total_q = await db.execute(select(func.count()).select_from(Level))
    total = total_q.scalar() or 0

    done_q = await db.execute(
        select(func.count())
        .select_from(UserProgress)
        .where(UserProgress.user_id == user_id, UserProgress.status == ProgressStatus.completed)
    )
    done = done_q.scalar() or 0

    by_track_q = await db.execute(
        select(Language.code, func.count())
        .select_from(UserProgress)
        .join(Level, Level.id == UserProgress.level_id)
        .join(Track, Track.id == Level.track_id)
        .join(Language, Language.id == Track.language_id)
        .where(UserProgress.user_id == user_id, UserProgress.status == ProgressStatus.completed)
        .group_by(Language.code)
    )
    by_track = {code: cnt for code, cnt in by_track_q.all()}
    return {"total_levels": total, "completed_levels": done, "by_track": by_track}
