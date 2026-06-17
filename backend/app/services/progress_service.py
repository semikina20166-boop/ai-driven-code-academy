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


async def _open_level(db: AsyncSession, user_id: UUID, level_id: int) -> None:
    prog = await db.get(UserProgress, {"user_id": user_id, "level_id": level_id})
    if not prog:
        db.add(UserProgress(user_id=user_id, level_id=level_id, status=ProgressStatus.open, attempts=0))
    elif prog.status == ProgressStatus.locked:
        prog.status = ProgressStatus.open


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
    if nxt:
        await _open_level(db, user_id, nxt.id)
        return

    diff_q = await db.execute(select(Difficulty).where(Difficulty.id == level.difficulty_id))
    current_diff = diff_q.scalar_one_or_none()
    if not current_diff:
        return

    next_diff_q = await db.execute(
        select(Difficulty).where(Difficulty.sort_order == current_diff.sort_order + 1)
    )
    next_diff = next_diff_q.scalar_one_or_none()
    if not next_diff:
        return

    first_q = await db.execute(
        select(Level).where(
            Level.track_id == level.track_id,
            Level.difficulty_id == next_diff.id,
            Level.order_num == 1,
        )
    )
    first_of_next = first_q.scalar_one_or_none()
    if first_of_next:
        await _open_level(db, user_id, first_of_next.id)


async def reconcile_track_unlocks(db: AsyncSession, user_id: UUID, track_id: int) -> None:
    """Repair unlock chain for users who completed levels before cross-difficulty unlock existed."""
    completed_q = await db.execute(
        select(Level)
        .join(UserProgress, UserProgress.level_id == Level.id)
        .join(Difficulty, Difficulty.id == Level.difficulty_id)
        .where(
            UserProgress.user_id == user_id,
            UserProgress.status == ProgressStatus.completed,
            Level.track_id == track_id,
        )
        .order_by(Difficulty.sort_order, Level.order_num)
    )
    for level in completed_q.scalars().all():
        await unlock_next_level(db, user_id, level)


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
