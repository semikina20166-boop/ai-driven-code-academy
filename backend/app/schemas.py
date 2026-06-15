from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    display_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    display_name: str | None
    is_premium: bool = False

    model_config = {"from_attributes": True}


class LanguageOut(BaseModel):
    id: int
    code: str
    name: str

    model_config = {"from_attributes": True}


class TrackOut(BaseModel):
    id: int
    language_id: int
    # Legacy single field (fallback for older clients)
    title: str = ""
    description: str | None = None
    # Localized fields
    title_ru: str = ""
    title_en: str = ""
    title_kz: str = ""
    description_ru: str | None = None
    description_en: str | None = None
    description_kz: str | None = None
    language: LanguageOut | None = None

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_with_lang(cls, track, lang: str = "ru") -> "TrackOut":
        title_ru = track.title_ru or ""
        title_en = track.title_en or title_ru
        title_kz = track.title_kz or title_ru
        desc_ru = track.description_ru
        desc_en = track.description_en or desc_ru
        desc_kz = track.description_kz or desc_ru
        title_map = {"ru": title_ru, "en": title_en, "kz": title_kz}
        desc_map = {"ru": desc_ru, "en": desc_en, "kz": desc_kz}
        return cls(
            id=track.id,
            language_id=track.language_id,
            title=title_map.get(lang, title_ru),
            description=desc_map.get(lang, desc_ru),
            title_ru=title_ru,
            title_en=title_en,
            title_kz=title_kz,
            description_ru=desc_ru,
            description_en=desc_en,
            description_kz=desc_kz,
            language=LanguageOut.model_validate(track.language) if track.language else None,
        )


class LevelMapItem(BaseModel):
    id: int
    order_num: int
    title: str
    title_ru: str = ""
    title_en: str = ""
    title_kz: str = ""
    difficulty_code: str
    difficulty_name: str
    difficulty_name_ru: str = ""
    difficulty_name_en: str = ""
    difficulty_name_kz: str = ""
    status: str


class LevelDetailOut(BaseModel):
    id: int
    track_id: int
    order_num: int
    title: str
    title_ru: str = ""
    title_en: str = ""
    title_kz: str = ""
    task_text: str
    task_text_ru: str = ""
    task_text_en: str = ""
    task_text_kz: str = ""
    starter_code: str
    status: str
    allowed_concepts: list[str]
    difficulty_code: str
    difficulty_name: str
    difficulty_name_ru: str = ""
    difficulty_name_en: str = ""
    difficulty_name_kz: str = ""
    theory: str | None = None
    theory_ru: str | None = None
    theory_en: str | None = None
    theory_kz: str | None = None


class RunCodeRequest(BaseModel):
    level_id: int
    code: str


class CodeReviewRequest(BaseModel):
    level_id: int
    code: str


class CodeReviewResponse(BaseModel):
    review: str


class RunCodeResponse(BaseModel):
    passed: bool
    stdout: str = ""
    stderr: str = ""
    details: list[Any] = []


class AiHintRequest(BaseModel):
    level_id: int
    code: str
    error_message: str = ""


class AiHintResponse(BaseModel):
    hint: str


class ExamOut(BaseModel):
    id: int
    exam_type: str
    title: str
    title_ru: str = ""
    title_en: str = ""
    title_kz: str = ""
    description: str | None = None
    description_ru: str | None = None
    description_en: str | None = None
    description_kz: str | None = None
    pass_percent: int
    time_limit_min: int | None
    available: bool = False


class ExamQuestionOut(BaseModel):
    id: int
    order_num: int
    task_text: str
    task_text_ru: str = ""
    task_text_en: str = ""
    task_text_kz: str = ""
    starter_code: str


class StartExamResponse(BaseModel):
    attempt_id: int
    exam_id: int
    questions: list[ExamQuestionOut]


class SubmitExamAnswerRequest(BaseModel):
    question_id: int
    code: str


class SelectedTracksExamRequest(BaseModel):
    exam_id: int
    track_ids: list[int] = Field(min_length=1)


class ProgressSummary(BaseModel):
    total_levels: int
    completed_levels: int
    by_track: dict[str, int]


class LectureLevelOut(BaseModel):
    id: int
    order_num: int
    title: str
    title_ru: str = ""
    title_en: str = ""
    title_kz: str = ""
    difficulty_code: str
    difficulty_name: str
    difficulty_name_ru: str = ""
    difficulty_name_en: str = ""
    difficulty_name_kz: str = ""
    theory: str | None = None
    theory_ru: str | None = None
    theory_en: str | None = None
    theory_kz: str | None = None


class TrackLecturesOut(BaseModel):
    track_id: int
    language_code: str
    language_name: str
    levels: list[LectureLevelOut]
