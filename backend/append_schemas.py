
content = """

class TrackCreate(BaseModel):
    language_id: int
    title_ru: str = ""
    title_en: str = ""
    title_kz: str = ""
    description_ru: str | None = None
    description_en: str | None = None
    description_kz: str | None = None


class LevelCreate(BaseModel):
    track_id: int
    difficulty_id: int
    order_num: int
    title_ru: str = ""
    title_en: str = ""
    title_kz: str = ""
    task_text_ru: str = ""
    task_text_en: str = ""
    task_text_kz: str = ""
    starter_code: str = ""
    solution_tests: dict = {}
    allowed_concepts: list[str] = []
    theory_ru: str | None = None
    theory_en: str | None = None
    theory_kz: str | None = None


class ExamCreate(BaseModel):
    exam_type: str
    title_ru: str = ""
    title_en: str = ""
    title_kz: str = ""
    description_ru: str | None = None
    description_en: str | None = None
    description_kz: str | None = None
    pass_percent: int = 70
    time_limit_min: int | None = None
    max_attempts: int = 3
"""

with open("app/schemas.py", "a", encoding="utf-8") as f:
    f.write(content)
