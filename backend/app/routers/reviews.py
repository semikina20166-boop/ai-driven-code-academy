from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import CurrentUser
from app.database import get_db
from app.models import (
    CourseReview,
    Exam,
    ExamReview,
    Level,
    Track,
    UserExamAttempt,
    UserProgress,
)
from app.schemas import (
    AllReviewsOut,
    ExamReviewOut,
    ExamReviewsOut,
    ExamReviewSummary,
    ReviewCreate,
    ReviewOut,
    TrackReviewsOut,
    TrackReviewSummary,
)

router = APIRouter(prefix="/reviews", tags=["reviews"])


# ─────────────────────────────── helpers ──────────────────────────────────────

def _review_to_out(review: CourseReview, current_user_id) -> ReviewOut:
    return ReviewOut(
        id=review.id,
        user_id=str(review.user_id),
        display_name=review.user.display_name if review.user else None,
        track_id=review.track_id,
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at,
        updated_at=review.updated_at,
        is_own=(review.user_id == current_user_id),
    )


def _exam_review_to_out(review: ExamReview, current_user_id) -> ExamReviewOut:
    return ExamReviewOut(
        id=review.id,
        user_id=str(review.user_id),
        display_name=review.user.display_name if review.user else None,
        exam_id=review.exam_id,
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at,
        updated_at=review.updated_at,
        is_own=(review.user_id == current_user_id),
    )


def _avg(items) -> float | None:
    return round(sum(r.rating for r in items) / len(items), 2) if items else None


async def _check_track_completion(db: AsyncSession, user_id, track_id: int) -> bool:
    """Возвращает True, если пользователь завершил ВСЕ уровни трека."""
    total_q = await db.execute(
        select(func.count()).select_from(Level).where(Level.track_id == track_id)
    )
    total = total_q.scalar_one()
    if total == 0:
        return False

    completed_q = await db.execute(
        select(func.count())
        .select_from(UserProgress)
        .where(
            UserProgress.user_id == user_id,
            UserProgress.level_id.in_(select(Level.id).where(Level.track_id == track_id)),
            UserProgress.status == "completed",
        )
    )
    return completed_q.scalar_one() >= total


async def _check_exam_passed(db: AsyncSession, user_id, exam_id: int) -> bool:
    """Возвращает True, если пользователь хотя бы раз сдал экзамен."""
    q = await db.execute(
        select(func.count())
        .select_from(UserExamAttempt)
        .where(
            UserExamAttempt.user_id == user_id,
            UserExamAttempt.exam_id == exam_id,
            UserExamAttempt.passed == True,
        )
    )
    return q.scalar_one() > 0


# ─────────────────────── track reviews ────────────────────────────────────────

@router.get("/track/{track_id}", response_model=TrackReviewsOut)
async def get_track_reviews(
    track_id: int,
    lang: str = Query(default="ru", regex="^(ru|en|kz)$"),
    user: CurrentUser = None,
    db: AsyncSession = Depends(get_db),
):
    """Получить все отзывы по треку вместе с мета-информацией."""
    track = await db.get(Track, track_id)
    if not track:
        raise HTTPException(404, "Трек не найден")

    result = await db.execute(
        select(CourseReview)
        .where(CourseReview.track_id == track_id)
        .options(selectinload(CourseReview.user))
        .order_by(CourseReview.created_at.desc())
    )
    reviews_db = result.scalars().all()
    reviews_out = [_review_to_out(r, user.id) for r in reviews_db]
    can_review = await _check_track_completion(db, user.id, track_id)
    my_review_out = next((r for r in reviews_out if r.is_own), None)

    return TrackReviewsOut(
        track_id=track_id,
        average_rating=_avg(reviews_db),
        total_reviews=len(reviews_db),
        reviews=reviews_out,
        can_review=can_review,
        my_review=my_review_out,
    )


@router.post("/track/{track_id}", response_model=ReviewOut)
async def upsert_track_review(
    track_id: int,
    body: ReviewCreate,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Создать или обновить отзыв о треке (только после прохождения всех уровней)."""
    if not await db.get(Track, track_id):
        raise HTTPException(404, "Трек не найден")

    if not await _check_track_completion(db, user.id, track_id):
        raise HTTPException(403, "Оставить отзыв можно только после прохождения всех уровней курса")

    existing_q = await db.execute(
        select(CourseReview)
        .where(CourseReview.user_id == user.id, CourseReview.track_id == track_id)
        .options(selectinload(CourseReview.user))
    )
    review = existing_q.scalar_one_or_none()

    if review:
        review.rating = body.rating
        review.comment = body.comment
        review.updated_at = datetime.now(timezone.utc)
    else:
        review = CourseReview(user_id=user.id, track_id=track_id, rating=body.rating, comment=body.comment)
        db.add(review)
        await db.flush()
        await db.refresh(review, ["user"])

    await db.commit()
    await db.refresh(review)
    return _review_to_out(review, user.id)


@router.get("/track/{track_id}/my", response_model=ReviewOut | None)
async def get_my_track_review(
    track_id: int,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Получить свой отзыв о треке."""
    result = await db.execute(
        select(CourseReview)
        .where(CourseReview.user_id == user.id, CourseReview.track_id == track_id)
        .options(selectinload(CourseReview.user))
    )
    review = result.scalar_one_or_none()
    return _review_to_out(review, user.id) if review else None


# ─────────────────────── exam reviews ─────────────────────────────────────────

@router.get("/exam/{exam_id}", response_model=ExamReviewsOut)
async def get_exam_reviews(
    exam_id: int,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Получить все отзывы об экзамене."""
    if not await db.get(Exam, exam_id):
        raise HTTPException(404, "Экзамен не найден")

    result = await db.execute(
        select(ExamReview)
        .where(ExamReview.exam_id == exam_id)
        .options(selectinload(ExamReview.user))
        .order_by(ExamReview.created_at.desc())
    )
    reviews_db = result.scalars().all()
    reviews_out = [_exam_review_to_out(r, user.id) for r in reviews_db]
    can_review = await _check_exam_passed(db, user.id, exam_id)
    my_review_out = next((r for r in reviews_out if r.is_own), None)

    return ExamReviewsOut(
        exam_id=exam_id,
        average_rating=_avg(reviews_db),
        total_reviews=len(reviews_db),
        reviews=reviews_out,
        can_review=can_review,
        my_review=my_review_out,
    )


@router.post("/exam/{exam_id}", response_model=ExamReviewOut)
async def upsert_exam_review(
    exam_id: int,
    body: ReviewCreate,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Создать или обновить отзыв об экзамене (только после успешной сдачи)."""
    if not await db.get(Exam, exam_id):
        raise HTTPException(404, "Экзамен не найден")

    if not await _check_exam_passed(db, user.id, exam_id):
        raise HTTPException(403, "Оставить отзыв можно только после успешной сдачи экзамена")

    existing_q = await db.execute(
        select(ExamReview)
        .where(ExamReview.user_id == user.id, ExamReview.exam_id == exam_id)
        .options(selectinload(ExamReview.user))
    )
    review = existing_q.scalar_one_or_none()

    if review:
        review.rating = body.rating
        review.comment = body.comment
        review.updated_at = datetime.now(timezone.utc)
    else:
        review = ExamReview(user_id=user.id, exam_id=exam_id, rating=body.rating, comment=body.comment)
        db.add(review)
        await db.flush()
        await db.refresh(review, ["user"])

    await db.commit()
    await db.refresh(review)
    return _exam_review_to_out(review, user.id)


@router.get("/exam/{exam_id}/my", response_model=ExamReviewOut | None)
async def get_my_exam_review(
    exam_id: int,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Получить свой отзыв об экзамене."""
    result = await db.execute(
        select(ExamReview)
        .where(ExamReview.user_id == user.id, ExamReview.exam_id == exam_id)
        .options(selectinload(ExamReview.user))
    )
    review = result.scalar_one_or_none()
    return _exam_review_to_out(review, user.id) if review else None


# ─────────────────────── all reviews (global page) ────────────────────────────

@router.get("/all", response_model=AllReviewsOut)
async def get_all_reviews(
    lang: str = Query(default="ru", regex="^(ru|en|kz)$"),
    user: CurrentUser = None,
    db: AsyncSession = Depends(get_db),
):
    """Получить все отзывы по всем трекам и экзаменам (для страницы отзывов)."""
    # ── Track reviews ──
    tracks_q = await db.execute(select(Track).order_by(Track.id))
    tracks = tracks_q.scalars().all()

    track_summaries: list[TrackReviewSummary] = []
    for track in tracks:
        r_q = await db.execute(
            select(CourseReview)
            .where(CourseReview.track_id == track.id)
            .options(selectinload(CourseReview.user))
            .order_by(CourseReview.created_at.desc())
        )
        reviews_db = r_q.scalars().all()
        reviews_out = [_review_to_out(r, user.id) for r in reviews_db]

        title_map = {"ru": track.title_ru, "en": track.title_en or track.title_ru, "kz": track.title_kz or track.title_ru}
        track_summaries.append(TrackReviewSummary(
            track_id=track.id,
            track_title=title_map.get(lang, track.title_ru) or f"Трек #{track.id}",
            average_rating=_avg(reviews_db),
            total_reviews=len(reviews_db),
            reviews=reviews_out,
        ))

    # ── Exam reviews ──
    exams_q = await db.execute(select(Exam).order_by(Exam.id))
    exams = exams_q.scalars().all()

    exam_summaries: list[ExamReviewSummary] = []
    for exam in exams:
        r_q = await db.execute(
            select(ExamReview)
            .where(ExamReview.exam_id == exam.id)
            .options(selectinload(ExamReview.user))
            .order_by(ExamReview.created_at.desc())
        )
        reviews_db = r_q.scalars().all()
        reviews_out = [_exam_review_to_out(r, user.id) for r in reviews_db]

        title_map = {"ru": exam.title_ru, "en": exam.title_en or exam.title_ru, "kz": exam.title_kz or exam.title_ru}
        exam_summaries.append(ExamReviewSummary(
            exam_id=exam.id,
            exam_title=title_map.get(lang, exam.title_ru) or f"Экзамен #{exam.id}",
            exam_type=exam.exam_type.value,
            average_rating=_avg(reviews_db),
            total_reviews=len(reviews_db),
            reviews=reviews_out,
        ))

    total = sum(s.total_reviews for s in track_summaries) + sum(s.total_reviews for s in exam_summaries)

    return AllReviewsOut(
        tracks=track_summaries,
        exams=exam_summaries,
        total_reviews=total,
    )
