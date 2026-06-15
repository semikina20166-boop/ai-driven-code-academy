from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.database import engine
from app.routers import ai_hints, auth, exams, levels, progress, tracks, lectures

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


@app.exception_handler(SQLAlchemyError)
async def database_error_handler(_request: Request, _exc: SQLAlchemyError):
    return JSONResponse(
        status_code=503,
        content={
            "detail": (
                "База данных недоступна. Запустите PostgreSQL, создайте ai_academy "
                "и выполните database/schema.sql и seed.sql. Проверьте DATABASE_URL в backend/.env"
            )
        },
    )


@app.on_event("startup")
async def check_database():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))

            # ── Users table migrations ────────────────────────────────────
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_premium BOOLEAN DEFAULT FALSE;"))
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS hints_used_today INT DEFAULT 0;"))
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_hint_date DATE DEFAULT CURRENT_DATE;"))

            # ── Difficulties: add EN/KZ name columns ─────────────────────
            await conn.execute(text("ALTER TABLE difficulties ADD COLUMN IF NOT EXISTS name_en VARCHAR(32) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE difficulties ADD COLUMN IF NOT EXISTS name_kz VARCHAR(32) NOT NULL DEFAULT '';"))
            # Populate EN/KZ for difficulties
            await conn.execute(text("""
                UPDATE difficulties SET
                    name_en = CASE code WHEN 'easy' THEN 'Beginner' WHEN 'medium' THEN 'Intermediate' WHEN 'hard' THEN 'Advanced' ELSE name_ru END,
                    name_kz = CASE code WHEN 'easy' THEN 'Бастапқы' WHEN 'medium' THEN 'Орташа' WHEN 'hard' THEN 'Жоғары' ELSE name_ru END
                WHERE name_en = '' OR name_kz = ''
            """))

            # ── Tracks: rename old columns, add localized columns ─────────
            # Add new localized title/description columns
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS title_ru VARCHAR(128) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS title_en VARCHAR(128) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS title_kz VARCHAR(128) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS description_ru TEXT;"))
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS description_en TEXT;"))
            await conn.execute(text("ALTER TABLE tracks ADD COLUMN IF NOT EXISTS description_kz TEXT;"))
            # Back-fill from old title/description columns if they exist
            await conn.execute(text("""
                UPDATE tracks SET
                    title_ru = COALESCE(NULLIF(title_ru,''), title, ''),
                    title_en = COALESCE(NULLIF(title_en,''), REPLACE(title, ' — трек', ' — Track'), title, ''),
                    title_kz = COALESCE(NULLIF(title_kz,''), REPLACE(title, ' — трек', ' — тред'), title, ''),
                    description_ru = COALESCE(description_ru, description),
                    description_en = COALESCE(description_en, description),
                    description_kz = COALESCE(description_kz, description)
                WHERE title_ru = '' OR title_en = '' OR title_kz = ''
            """))

            # ── Levels: add localized columns ─────────────────────────────
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS title_ru VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS title_en VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS title_kz VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS task_text_ru TEXT NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS task_text_en TEXT NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS task_text_kz TEXT NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS theory_ru TEXT;"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS theory_en TEXT;"))
            await conn.execute(text("ALTER TABLE levels ADD COLUMN IF NOT EXISTS theory_kz TEXT;"))
            # Back-fill from old single-language columns
            await conn.execute(text("""
                UPDATE levels SET
                    title_ru = COALESCE(NULLIF(title_ru,''), title, ''),
                    title_en = COALESCE(NULLIF(title_en,''), title, ''),
                    title_kz = COALESCE(NULLIF(title_kz,''), title, ''),
                    task_text_ru = COALESCE(NULLIF(task_text_ru,''), task_text, ''),
                    task_text_en = COALESCE(NULLIF(task_text_en,''), task_text, ''),
                    task_text_kz = COALESCE(NULLIF(task_text_kz,''), task_text, ''),
                    theory_ru = COALESCE(theory_ru, theory),
                    theory_en = COALESCE(theory_en, theory),
                    theory_kz = COALESCE(theory_kz, theory)
                WHERE title_ru = '' OR task_text_ru = ''
            """))

            # ── Exams: add localized columns ──────────────────────────────
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS title_ru VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS title_en VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS title_kz VARCHAR(255) NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS description_ru TEXT;"))
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS description_en TEXT;"))
            await conn.execute(text("ALTER TABLE exams ADD COLUMN IF NOT EXISTS description_kz TEXT;"))
            # Back-fill exams from old columns
            await conn.execute(text("""
                UPDATE exams SET
                    title_ru = COALESCE(NULLIF(title_ru,''), title, ''),
                    title_en = COALESCE(NULLIF(title_en,''), title, ''),
                    title_kz = COALESCE(NULLIF(title_kz,''), title, ''),
                    description_ru = COALESCE(description_ru, description),
                    description_en = COALESCE(description_en, description),
                    description_kz = COALESCE(description_kz, description)
                WHERE title_ru = ''
            """))

            # ── ExamQuestions: add localized columns ──────────────────────
            await conn.execute(text("ALTER TABLE exam_questions ADD COLUMN IF NOT EXISTS task_text_ru TEXT NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE exam_questions ADD COLUMN IF NOT EXISTS task_text_en TEXT NOT NULL DEFAULT '';"))
            await conn.execute(text("ALTER TABLE exam_questions ADD COLUMN IF NOT EXISTS task_text_kz TEXT NOT NULL DEFAULT '';"))
            # Back-fill from old task_text column
            await conn.execute(text("""
                UPDATE exam_questions SET
                    task_text_ru = COALESCE(NULLIF(task_text_ru,''), task_text, ''),
                    task_text_en = COALESCE(NULLIF(task_text_en,''), task_text, ''),
                    task_text_kz = COALESCE(NULLIF(task_text_kz,''), task_text, '')
                WHERE task_text_ru = ''
            """))

            # ── Populate rich theory for Python Easy L1 on all 3 languages ──
            theory_py_easy1_ru = (
                "### 📖 Лекция: Введение в функции и переменные\n\n"
                "Функции в Python объявляются с помощью ключевого слова **`def`**, "
                "за которым следует имя функции, круглые скобки `()` и двоеточие `:`.\n\n"
                "Пример объявления функции:\n"
                "```python\ndef greet(name):\n    print('Привет, ' + name)\n```\n\n"
                "**Возврат значения:** Используется ключевое слово **`return`**. "
                "Если `return` отсутствует, функция возвращает `None`.\n\n"
                "**Сложение чисел:** Для сложения используется оператор **`+`**:\n"
                "```python\nresult = 5 + 10  # result = 15\n```\n\n"
                "**Задание:** Напишите тело функции `sum_two(a, b)`, которая вернёт сумму `a` и `b`."
            )
            theory_py_easy1_en = (
                "### 📖 Lecture: Introduction to Functions and Variables\n\n"
                "Functions in Python are declared with the **`def`** keyword, "
                "followed by the function name, parentheses `()`, and a colon `:`.\n\n"
                "Example function declaration:\n"
                "```python\ndef greet(name):\n    print('Hello, ' + name)\n```\n\n"
                "**Returning a value:** Use the **`return`** keyword. "
                "If `return` is absent, the function returns `None`.\n\n"
                "**Adding numbers:** Use the **`+`** operator:\n"
                "```python\nresult = 5 + 10  # result = 15\n```\n\n"
                "**Task:** Write the body of `sum_two(a, b)` that returns the sum of `a` and `b`."
            )
            theory_py_easy1_kz = (
                "### 📖 Дәріс: Функциялар мен айнымалыларға кіріспе\n\n"
                "Python-да функциялар **`def`** кілт сөзімен жарияланады, "
                "одан кейін функция атауы, жақша `()` және қос нүкте `:` келеді.\n\n"
                "Функцияны жариялау мысалы:\n"
                "```python\ndef greet(name):\n    print('Сәлем, ' + name)\n```\n\n"
                "**Мән қайтару:** **`return`** кілт сөзі қолданылады. "
                "`return` болмаса, функция `None` қайтарады.\n\n"
                "**Сандарды қосу:** **`+`** операторы пайдаланылады:\n"
                "```python\nnәтиже = 5 + 10  # 15\n```\n\n"
                "**Тапсырма:** `sum_two(a, b)` функциясының денесін жазыңыз, ол `a` мен `b` қосындысын қайтарады."
            )
            await conn.execute(text(
                "UPDATE levels SET theory_ru = :ru, theory_en = :en, theory_kz = :kz "
                "FROM tracks tr JOIN languages l ON l.id = tr.language_id "
                "JOIN difficulties d ON d.id = levels.difficulty_id "
                "WHERE levels.track_id = tr.id AND l.code = 'python' AND d.code = 'easy' AND levels.order_num = 1 "
                "AND (levels.theory_ru IS NULL OR levels.theory_ru = '')"
            ), {"ru": theory_py_easy1_ru, "en": theory_py_easy1_en, "kz": theory_py_easy1_kz})

            # ── Generic theory for all levels without theory ──────────────
            generic_ru = (
                "### 📖 Лекция к задаче\n\n"
                "В этом уроке закрепляются навыки решения задач на практике. "
                "Вам понадобятся концепции из раздела «Допустимые термины».\n\n"
                "**Ключевые рекомендации:**\n"
                "- Внимательно читайте условие задачи.\n"
                "- Разбейте алгоритм на логические блоки.\n"
                "- Если возникли сложности, обратитесь к **ИИ-наставнику** справа.\n\n"
                "*Удачи в решении задачи!*"
            )
            generic_en = (
                "### 📖 Lecture for the Task\n\n"
                "This lesson consolidates practical problem-solving skills. "
                "You will need the concepts listed in 'Allowed Terms'.\n\n"
                "**Key recommendations:**\n"
                "- Read the task conditions carefully.\n"
                "- Break the algorithm into logical blocks.\n"
                "- If you get stuck, ask the **AI Mentor** on the right.\n\n"
                "*Good luck solving the task!*"
            )
            generic_kz = (
                "### 📖 Тапсырмаға дәріс\n\n"
                "Бұл сабақта практикалық есеп шешу дағдылары бекітіледі. "
                "«Рұқсат етілген терминдер» бөліміндегі тұжырымдамалар қажет болады.\n\n"
                "**Негізгі ұсыныстар:**\n"
                "- Тапсырма шарттарын мұқият оқыңыз.\n"
                "- Алгоритмді логикалық блоктарға бөліңіз.\n"
                "- Қиындық туса, оң жақтағы **ИИ Тәлімгерге** жүгініңіз.\n\n"
                "*Тапсырманы шешуде сәттілік!*"
            )
            await conn.execute(text(
                "UPDATE levels SET theory_ru = :ru, theory_en = :en, theory_kz = :kz "
                "WHERE (theory_ru IS NULL OR theory_ru = '') "
                "AND (theory_en IS NULL OR theory_en = '') "
                "AND (theory_kz IS NULL OR theory_kz = '')"
            ), {"ru": generic_ru, "en": generic_en, "kz": generic_kz})

    except Exception as exc:
        import logging
        logging.getLogger("uvicorn.error").warning(
            "Ошибка при проверке/миграции базы данных: %s — регистрация или уровни могут работать неверно", exc
        )

app.include_router(auth.router)
app.include_router(tracks.router)
app.include_router(levels.router)
app.include_router(progress.router)
app.include_router(ai_hints.router)
app.include_router(exams.router)
app.include_router(lectures.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-driven-code-academy", "version": "2.0.0"}
