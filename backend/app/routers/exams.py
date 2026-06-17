from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import CurrentUser
from app.database import get_db
from app.models import (
    Exam,
    ExamDifficultyBlock,
    ExamQuestion,
    ExamType,
    ProgressStatus,
    UserExamAttempt,
    UserExamAnswer,
    UserSelectedTracksForExam,
)
from app.schemas import (
    ExamOut,
    ExamQuestionOut,
    SelectedTracksExamRequest,
    StartExamResponse,
    SubmitExamAnswerRequest,
)
from app.services.code_runner import run_tests_for_language
from app.services.progress_service import count_completed_in_block, progress_summary

router = APIRouter(prefix="/exams", tags=["exams"])


async def _get_exam_attempt_stats(db: AsyncSession, user_id, exam_id: int) -> tuple[bool, int | None, int]:
    attempts_q = await db.execute(
        select(UserExamAttempt).where(
            UserExamAttempt.user_id == user_id,
            UserExamAttempt.exam_id == exam_id,
        )
    )
    attempts = attempts_q.scalars().all()
    finished = [a for a in attempts if a.finished_at is not None]
    passed = any(a.passed for a in finished if a.passed is not None)
    scores = [a.score for a in finished if a.score is not None]
    best_score = max(scores) if scores else None
    return passed, best_score, len(attempts)


def _pick(ru: str, en: str, kz: str, lang: str) -> str:
    ru = ru or ""
    m = {"ru": ru, "en": en or ru, "kz": kz or ru}
    return m.get(lang, ru)


def _exam_out(
    exam: Exam,
    available: bool,
    lang: str,
    *,
    passed: bool = False,
    best_score: int | None = None,
    attempts_used: int = 0,
) -> ExamOut:
    title_ru = exam.title_ru or ""
    title_en = exam.title_en or title_ru
    title_kz = exam.title_kz or title_ru
    desc_ru = exam.description_ru
    desc_en = exam.description_en or desc_ru
    desc_kz = exam.description_kz or desc_ru
    return ExamOut(
        id=exam.id,
        exam_type=exam.exam_type.value,
        title=_pick(title_ru, title_en, title_kz, lang),
        title_ru=title_ru,
        title_en=title_en,
        title_kz=title_kz,
        description=_pick(desc_ru or "", desc_en or "", desc_kz or "", lang) or None,
        description_ru=desc_ru,
        description_en=desc_en,
        description_kz=desc_kz,
        pass_percent=exam.pass_percent,
        time_limit_min=exam.time_limit_min,
        available=available,
        passed=passed,
        best_score=best_score,
        attempts_used=attempts_used,
    )


@router.get("/available", response_model=list[ExamOut])
async def available_exams(
    user: CurrentUser,
    lang: str = Query(default="ru", regex="^(ru|en|kz)$"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Exam).order_by(Exam.id))
    exams = result.scalars().all()
    out: list[ExamOut] = []

    summary = await progress_summary(db, user.id)
    total_completed = summary["completed_levels"]

    for exam in exams:
        available = False
        if exam.exam_type == ExamType.difficulty_block:
            block = await db.get(ExamDifficultyBlock, exam.id)
            if block:
                done, total = await count_completed_in_block(
                    db, user.id, block.track_id, block.difficulty_id
                )
                available = total > 0 and done >= total
        elif exam.exam_type == ExamType.selected_tracks:
            available = total_completed >= 5
        elif exam.exam_type == ExamType.final:
            available = total_completed >= 30

        passed, best_score, attempts_used = await _get_exam_attempt_stats(db, user.id, exam.id)
        out.append(_exam_out(exam, available, lang, passed=passed, best_score=best_score, attempts_used=attempts_used))
    return out


@router.post("/{exam_id}/start", response_model=StartExamResponse)
async def start_exam(
    exam_id: int,
    user: CurrentUser,
    lang: str = Query(default="ru", regex="^(ru|en|kz)$"),
    db: AsyncSession = Depends(get_db),
):
    exam = await db.get(Exam, exam_id)
    if not exam:
        raise HTTPException(404, "Экзамен не найден")

    if exam.exam_type == ExamType.selected_tracks and not user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Экзамен по выбору доступен только для пользователей с Premium-подпиской."
        )

    available_list = await available_exams(user, lang=lang, db=db)
    match = next((e for e in available_list if e.id == exam_id), None)
    if not match or not match.available:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Экзамен пока недоступен")

    attempts_q = await db.execute(
        select(UserExamAttempt).where(
            UserExamAttempt.user_id == user.id,
            UserExamAttempt.exam_id == exam_id,
        )
    )
    attempts = attempts_q.scalars().all()
    if len(attempts) >= exam.max_attempts:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Исчерпаны попытки экзамена")

    attempt = UserExamAttempt(user_id=user.id, exam_id=exam_id)
    db.add(attempt)
    await db.flush()

    q = await db.execute(
        select(ExamQuestion)
        .where(ExamQuestion.exam_id == exam_id)
        .order_by(ExamQuestion.order_num)
    )
    questions = []
    for eq in q.scalars().all():
        task_ru = eq.task_text_ru or ""
        task_en = eq.task_text_en or task_ru
        task_kz = eq.task_text_kz or task_ru
        questions.append(
            ExamQuestionOut(
                id=eq.id,
                order_num=eq.order_num,
                task_text=_pick(task_ru, task_en, task_kz, lang),
                task_text_ru=task_ru,
                task_text_en=task_en,
                task_text_kz=task_kz,
                starter_code=eq.starter_code,
            )
        )
    await db.commit()

    return StartExamResponse(attempt_id=attempt.id, exam_id=exam_id, questions=questions)


@router.post("/attempt/{attempt_id}/submit")
async def submit_answer(
    attempt_id: int,
    body: SubmitExamAnswerRequest,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    attempt = await db.get(UserExamAttempt, attempt_id)
    if not attempt or attempt.user_id != user.id:
        raise HTTPException(404, "Попытка не найдена")
    if attempt.finished_at:
        raise HTTPException(400, "Попытка уже завершена")

    question = await db.get(ExamQuestion, body.question_id)
    if not question or question.exam_id != attempt.exam_id:
        raise HTTPException(404, "Вопрос не найден")

    test_result = run_tests_for_language(body.code, question.tests)
    answer = UserExamAnswer(
        attempt_id=attempt_id,
        question_id=question.id,
        submitted_code=body.code,
        test_result=test_result,
        passed=test_result.get("passed", False),
    )
    db.add(answer)
    await db.commit()
    return test_result


@router.post("/attempt/{attempt_id}/finish")
async def finish_exam(attempt_id: int, user: CurrentUser, db: AsyncSession = Depends(get_db)):
    attempt = await db.get(UserExamAttempt, attempt_id)
    if not attempt or attempt.user_id != user.id:
        raise HTTPException(404, "Попытка не найдена")

    exam = await db.get(Exam, attempt.exam_id)
    if not exam:
        raise HTTPException(404, "Экзамен не найден")

    answers_q = await db.execute(
        select(UserExamAnswer).where(UserExamAnswer.attempt_id == attempt_id)
    )
    answers = answers_q.scalars().all()
    questions_q = await db.execute(
        select(ExamQuestion).where(ExamQuestion.exam_id == exam.id)
    )
    total_questions = len(questions_q.scalars().all())
    if total_questions == 0:
        raise HTTPException(400, "У экзамена нет вопросов")

    passed_count = sum(1 for a in answers if a.passed)
    score = int(round(100 * passed_count / total_questions))
    attempt.score = score
    attempt.passed = score >= exam.pass_percent
    attempt.finished_at = datetime.now(timezone.utc)
    await db.commit()

    return {
        "attempt_id": attempt_id,
        "score": score,
        "passed": attempt.passed,
        "pass_percent_required": exam.pass_percent,
    }


@router.post("/selected-tracks/register")
async def register_selected_tracks(
    body: SelectedTracksExamRequest,
    user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    exam = await db.get(Exam, body.exam_id)
    if not exam or exam.exam_type != ExamType.selected_tracks:
        raise HTTPException(404, "Экзамен по выбранным курсам не найден")

    existing = await db.get(UserSelectedTracksForExam, {"user_id": user.id, "exam_id": body.exam_id})
    if existing:
        existing.track_ids = body.track_ids
    else:
        db.add(UserSelectedTracksForExam(user_id=user.id, exam_id=body.exam_id, track_ids=body.track_ids))
    await db.commit()
    return {"message": "Курсы сохранены", "track_ids": body.track_ids}
