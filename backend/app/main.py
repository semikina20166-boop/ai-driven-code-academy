from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError

from app.config import settings
from app.database import engine
from app.routers import ai_hints, auth, exams, levels, progress, tracks, lectures, reviews, languages

app = FastAPI(
    title="AI-Driven Code Academy API",
    description="Backend для интерактивного тренажёра изучения языков программирования",
    version="2.0.0",
)

_origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(OperationalError)
async def database_error_handler(_request: Request, _exc: OperationalError):
    return JSONResponse(
        status_code=503,
        content={
            "detail": (
                "База данных недоступна. Запустите PostgreSQL, создайте ai_academy "
                "и выполните database/schema.sql и seed.sql. Проверьте DATABASE_URL в backend/.env"
            )
        },
    )

@app.exception_handler(IntegrityError)
async def integrity_error_handler(_request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"detail": f"Ошибка данных: возможно, указан неверный ID (например, несуществующий Language ID). Детали: {exc.orig}"}
    )


@app.on_event("startup")
async def check_database():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))

            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_premium BOOLEAN DEFAULT FALSE;"))
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS hints_used_today INT DEFAULT 0;"))
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_hint_date DATE DEFAULT CURRENT_DATE;"))

            await conn.execute(text("ALTER TABLE difficulties ADD COLUMN IF NOT EXISTS name_en VARCHAR(32) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE difficulties ADD COLUMN IF NOT EXISTS name_kz VARCHAR(32) NOT NULL DEFAULT '';"))
            await conn.execute(text("""
                UPDATE difficulties SET
                    name_en = CASE code WHEN 'easy' THEN 'Beginner' WHEN 'medium' THEN 'Intermediate' WHEN 'hard' THEN 'Advanced' ELSE name_ru END,
                    name_kz = CASE code WHEN 'easy' THEN 'Бастапқы' WHEN 'medium' THEN 'Орташа' WHEN 'hard' THEN 'Жоғары' ELSE name_ru END
                WHERE name_en = '' OR name_kz = ''
            """))

            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS title_ru VARCHAR(128) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS title_en VARCHAR(128) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS title_kz VARCHAR(128) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS description_ru TEXT;"))
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS description_en TEXT;"))
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS description_kz TEXT;"))

            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS title_ru VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS title_en VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS title_kz VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS task_text_ru TEXT NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS task_text_en TEXT NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS task_text_kz TEXT NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS theory_ru TEXT;"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS theory_en TEXT;"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS theory_kz TEXT;"))

            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS title_ru VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS title_en VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS title_kz VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS description_ru TEXT;"))
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS description_en TEXT;"))
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS description_kz TEXT;"))

            await conn.execute(text("ALTER TABLE exam_questions ADD COLUMN IF NOT EXISTS task_text_ru TEXT NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE exam_questions ADD COLUMN IF NOT EXISTS task_text_en TEXT NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE exam_questions ADD COLUMN IF NOT EXISTS task_text_kz TEXT NOT NULL DEFAULT '';"))

            # ── course_reviews ────────────────────────────────────────────────
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS course_reviews (
                    id          SERIAL PRIMARY KEY,
                    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    track_id    INT  NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
                    rating      SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
                    comment     TEXT,
                    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
                    updated_at  TIMESTAMPTZ,
                    UNIQUE (user_id, track_id)
                )
            """))
            await conn.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_course_reviews_track ON course_reviews (track_id)"
            ))

            # ── exam_reviews ──────────────────────────────────────────────────
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS exam_reviews (
                    id          SERIAL PRIMARY KEY,
                    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    exam_id     INT  NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
                    rating      SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
                    comment     TEXT,
                    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
                    updated_at  TIMESTAMPTZ,
                    UNIQUE (user_id, exam_id)
                )
            """))
            await conn.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_exam_reviews_exam ON exam_reviews (exam_id)"
            ))

        await _populate_level_theory()
    except Exception as exc:
        import logging
        logging.getLogger("uvicorn.error").warning(
            "Ошибка при проверке/миграции базы данных: %s — регистрация или уровни могут работать неверно", exc
        )


async def _populate_level_theory() -> None:
    try:
        from scripts.generate_seed import TASKS
    except ImportError:
        return
        
    try:
        async with engine.begin() as conn:
            from sqlalchemy import text
            
            # Fetch levels to update them directly
            result = await conn.execute(text(
                "SELECT l.id, d.code as diff_code, l.order_num, lang.code as lang_code, lang.name as lang_name "
                "FROM levels l "
                "JOIN difficulties d ON l.difficulty_id = d.id "
                "JOIN tracks t ON l.track_id = t.id "
                "JOIN languages lang ON t.language_id = lang.id"
            ))
            levels = result.all()
            
            for row in levels:
                level_id = row.id
                diff = row.diff_code
                num = row.order_num
                l_code = row.lang_code
                l_name = row.lang_name
                
                if diff not in TASKS or num not in TASKS[diff]:
                    continue
                    
                task = TASKS[diff][num]
                code_ex = task["starter"].get(l_code, "")
                concepts = ", ".join(task["concepts"])
                
                theory_ru = (
                    f"### 📖 Лекция: {task['ru']}\n\n"
                    f"В этом задании вам нужно реализовать функцию `{task['name']}`.\n\n"
                    f"**Разрешенные концепции:** {concepts}\n\n"
                    f"### ⚙️ Пример синтаксиса ({l_name}):\n"
                    f"``` {l_code}\n"
                    f"{code_ex}\n"
                    f"```\n\n"
                    f"Если у вас возникнут трудности, обратитесь к ИИ-наставнику!"
                )
                theory_en = (
                    f"### 📖 Lecture: {task['en']}\n\n"
                    f"In this task you need to implement the function `{task['name']}`.\n\n"
                    f"**Allowed concepts:** {concepts}\n\n"
                    f"### ⚙️ Syntax Example ({l_name}):\n"
                    f"``` {l_code}\n"
                    f"{code_ex}\n"
                    f"```\n\n"
                    f"If you get stuck, ask the AI Mentor!"
                )
                theory_kz = (
                    f"### 📖 Дәріс: {task['kz']}\n\n"
                    f"Бұл тапсырмада сіз `{task['name']}` функциясын іске асыруыңыз керек.\n\n"
                    f"**Рұқсат етілген ұғымдар:** {concepts}\n\n"
                    f"### ⚙️ Синтаксис мысалы ({l_name}):\n"
                    f"``` {l_code}\n"
                    f"{code_ex}\n"
                    f"```\n\n"
                    f"Егер сізде қиындықтар туындаса, ИИ-тәлімгерге хабарласыңыз!"
                )
                
                await conn.execute(text(
                    "UPDATE levels SET theory_ru = :ru, theory_en = :en, theory_kz = :kz "
                    "WHERE id = :id AND (theory_ru IS NULL OR theory_ru = '' OR theory_ru LIKE '%Закрепляются%')"
                ), {"ru": theory_ru, "en": theory_en, "kz": theory_kz, "id": level_id})
                
    except Exception as exc:
        import logging
        logging.getLogger("uvicorn.error").warning("Не удалось заполнить теорию: %s", exc)


app.include_router(auth.router)
app.include_router(tracks.router)
app.include_router(levels.router)
app.include_router(progress.router)
app.include_router(ai_hints.router)
app.include_router(exams.router)
app.include_router(lectures.router)
app.include_router(reviews.router)
app.include_router(languages.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-driven-code-academy", "version": "2.0.0"}
