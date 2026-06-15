import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    ARRAY,
    Boolean,
    DateTime,
    Date,
    Enum,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ProgressStatus(str, enum.Enum):
    locked = "locked"
    open = "open"
    completed = "completed"


class ExamType(str, enum.Enum):
    difficulty_block = "difficulty_block"
    selected_tracks = "selected_tracks"
    final = "final"


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(16), unique=True)
    name: Mapped[str] = mapped_column(String(64))


class Difficulty(Base):
    __tablename__ = "difficulties"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(16), unique=True)
    name_ru: Mapped[str] = mapped_column(String(32))
    name_en: Mapped[str] = mapped_column(String(32), default="")
    name_kz: Mapped[str] = mapped_column(String(32), default="")
    sort_order: Mapped[int] = mapped_column(SmallInteger, default=0)


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    title_ru: Mapped[str] = mapped_column(String(128), default="")
    title_en: Mapped[str] = mapped_column(String(128), default="")
    title_kz: Mapped[str] = mapped_column(String(128), default="")
    description_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_kz: Mapped[str | None] = mapped_column(Text, nullable=True)

    language: Mapped["Language"] = relationship()
    levels: Mapped[list["Level"]] = relationship(back_populates="track")


class Level(Base):
    __tablename__ = "levels"
    __table_args__ = (UniqueConstraint("track_id", "difficulty_id", "order_num"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id"))
    difficulty_id: Mapped[int] = mapped_column(ForeignKey("difficulties.id"))
    order_num: Mapped[int] = mapped_column(SmallInteger)
    title_ru: Mapped[str] = mapped_column(String(255), default="")
    title_en: Mapped[str] = mapped_column(String(255), default="")
    title_kz: Mapped[str] = mapped_column(String(255), default="")
    task_text_ru: Mapped[str] = mapped_column(Text, default="")
    task_text_en: Mapped[str] = mapped_column(Text, default="")
    task_text_kz: Mapped[str] = mapped_column(Text, default="")
    starter_code: Mapped[str] = mapped_column(Text)
    solution_tests: Mapped[dict] = mapped_column(JSONB)
    allowed_concepts: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    theory_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    theory_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    theory_kz: Mapped[str | None] = mapped_column(Text, nullable=True)

    track: Mapped["Track"] = relationship(back_populates="levels")
    difficulty: Mapped["Difficulty"] = relationship()


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    display_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    hints_used_today: Mapped[int] = mapped_column(Integer, default=0)
    last_hint_date: Mapped[datetime.date] = mapped_column(Date, default=func.current_date())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UserProgress(Base):
    __tablename__ = "user_progress"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"), primary_key=True)
    status: Mapped[ProgressStatus] = mapped_column(
        Enum(ProgressStatus, name="progress_status", create_type=False)
    )
    attempts: Mapped[int] = mapped_column(SmallInteger, default=0)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(primary_key=True)
    exam_type: Mapped[ExamType] = mapped_column(Enum(ExamType, name="exam_type", create_type=False))
    title_ru: Mapped[str] = mapped_column(String(255), default="")
    title_en: Mapped[str] = mapped_column(String(255), default="")
    title_kz: Mapped[str] = mapped_column(String(255), default="")
    description_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_kz: Mapped[str | None] = mapped_column(Text, nullable=True)
    pass_percent: Mapped[int] = mapped_column(SmallInteger, default=70)
    time_limit_min: Mapped[int | None] = mapped_column(nullable=True)
    max_attempts: Mapped[int] = mapped_column(SmallInteger, default=3)

    questions: Mapped[list["ExamQuestion"]] = relationship(back_populates="exam")


class ExamDifficultyBlock(Base):
    __tablename__ = "exam_difficulty_blocks"

    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), primary_key=True)
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id"))
    difficulty_id: Mapped[int] = mapped_column(ForeignKey("difficulties.id"))


class ExamQuestion(Base):
    __tablename__ = "exam_questions"
    __table_args__ = (UniqueConstraint("exam_id", "order_num"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"))
    order_num: Mapped[int] = mapped_column(SmallInteger)
    task_text_ru: Mapped[str] = mapped_column(Text, default="")
    task_text_en: Mapped[str] = mapped_column(Text, default="")
    task_text_kz: Mapped[str] = mapped_column(Text, default="")
    starter_code: Mapped[str] = mapped_column(Text)
    tests: Mapped[dict] = mapped_column(JSONB)
    language_id: Mapped[int | None] = mapped_column(ForeignKey("languages.id"), nullable=True)

    exam: Mapped["Exam"] = relationship(back_populates="questions")


class UserExamAttempt(Base):
    __tablename__ = "user_exam_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"))
    score: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    passed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class UserExamAnswer(Base):
    __tablename__ = "user_exam_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("user_exam_attempts.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("exam_questions.id"))
    submitted_code: Mapped[str] = mapped_column(Text)
    test_result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UserSelectedTracksForExam(Base):
    __tablename__ = "user_selected_tracks_for_exam"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), primary_key=True)
    track_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
