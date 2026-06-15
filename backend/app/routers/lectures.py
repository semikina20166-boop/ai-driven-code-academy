from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import CurrentUser
from app.database import get_db
from app.models import Track, Level
from app.schemas import TrackLecturesOut, LectureLevelOut

router = APIRouter(prefix="/lectures", tags=["lectures"])


def _pick(ru: str, en: str, kz: str, lang: str) -> str:
    ru = ru or ""
    m = {"ru": ru, "en": en or ru, "kz": kz or ru}
    return m.get(lang, ru)


@router.get("", response_model=list[TrackLecturesOut])
async def get_lectures(
    user: CurrentUser,
    lang: str = Query(default="ru", regex="^(ru|en|kz)$"),
    db: AsyncSession = Depends(get_db),
):
    # Query tracks and prefetch language and levels with their difficulties
    result = await db.execute(
        select(Track)
        .options(
            selectinload(Track.language),
            selectinload(Track.levels).selectinload(Level.difficulty)
        )
        .order_by(Track.id)
    )
    tracks = result.scalars().all()

    out: list[TrackLecturesOut] = []

    for track in tracks:
        # Sort levels by difficulty sort_order, then order_num
        sorted_levels = sorted(
            track.levels,
            key=lambda l: (l.difficulty.sort_order, l.order_num)
        )

        levels_list: list[LectureLevelOut] = []
        for lvl in sorted_levels:
            is_hard = lvl.difficulty.code == "hard"

            title_ru = lvl.title_ru or ""
            title_en = lvl.title_en or title_ru
            title_kz = lvl.title_kz or title_ru

            diff_ru = lvl.difficulty.name_ru or ""
            diff_en = getattr(lvl.difficulty, "name_en", "") or diff_ru
            diff_kz = getattr(lvl.difficulty, "name_kz", "") or diff_ru

            # Hide theory text for free users if Hard difficulty
            if is_hard and not user.is_premium:
                theory_ru = theory_en = theory_kz = None
            else:
                theory_ru = lvl.theory_ru
                theory_en = lvl.theory_en or theory_ru
                theory_kz = lvl.theory_kz or theory_ru

            theory_for_lang = _pick(theory_ru or "", theory_en or "", theory_kz or "", lang) or None

            levels_list.append(
                LectureLevelOut(
                    id=lvl.id,
                    order_num=lvl.order_num,
                    title=_pick(title_ru, title_en, title_kz, lang),
                    title_ru=title_ru,
                    title_en=title_en,
                    title_kz=title_kz,
                    difficulty_code=lvl.difficulty.code,
                    difficulty_name=_pick(diff_ru, diff_en, diff_kz, lang),
                    difficulty_name_ru=diff_ru,
                    difficulty_name_en=diff_en,
                    difficulty_name_kz=diff_kz,
                    theory=theory_for_lang,
                    theory_ru=theory_ru,
                    theory_en=theory_en,
                    theory_kz=theory_kz,
                )
            )

        out.append(
            TrackLecturesOut(
                track_id=track.id,
                language_code=track.language.code if track.language else "unknown",
                language_name=track.language.name if track.language else (track.title_ru or ""),
                levels=levels_list
            )
        )

    return out
