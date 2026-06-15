from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import CurrentUser
from app.database import get_db
from app.models import Track
from app.schemas import TrackOut
from app.services.progress_service import ensure_first_level_open

router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("", response_model=list[TrackOut])
async def list_tracks(
    lang: str = Query(default="ru", regex="^(ru|en|kz)$"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Track).options(selectinload(Track.language)).order_by(Track.id))
    tracks = result.scalars().all()
    return [TrackOut.from_orm_with_lang(t, lang) for t in tracks]


@router.post("/{track_id}/start")
async def start_track(track_id: int, user: CurrentUser, db: AsyncSession = Depends(get_db)):
    track = await db.get(Track, track_id)
    if not track:
        raise HTTPException(404, "Трек не найден")
    await ensure_first_level_open(db, user.id, track_id)
    await db.commit()
    return {"message": "Первый уровень трека открыт", "track_id": track_id}
