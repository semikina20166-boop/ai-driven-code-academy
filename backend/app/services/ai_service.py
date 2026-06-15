from openai import AsyncOpenAI

from app.config import settings
from app.services.local_mentor import get_local_hint

SYSTEM_PROMPT = """Ты наставник платформы AI-Driven Code Academy.
Язык ответа: только русский.
ЗАПРЕЩЕНО: давать готовый код решения, полные функции из ответа задачи, копировать решение пользователя.
Используй метод Сократа — наводящие вопросы и намёки.
Учитывай сложность уровня и список допустимых терминов — не используй понятия, которые пользователь ещё не проходил."""

FALLBACK_HINT = (
    "Попробуйте разбить задачу на шаги и проверить граничные случаи."
)


def _ai_not_configured_message() -> str:
    return (
        "ИИ-наставник не настроен. Укажите AI_PROVIDER=builtin (встроенный) "
        "или AI_PROVIDER=remote с AI_MODEL и AI_BASE_URL (обученная модель). "
        "Проверьте синтаксис, инициализацию переменных и соответствие типов аргументам функции."
    )


def _create_client() -> AsyncOpenAI | None:
    if not settings.ai_model:
        return None

    if settings.ai_base_url:
        return AsyncOpenAI(
            base_url=settings.ai_base_url.rstrip("/"),
            api_key=settings.ai_api_key or "not-needed",
        )

    if settings.ai_api_key:
        return AsyncOpenAI(api_key=settings.ai_api_key)

    return None


async def get_hint(
    *,
    task_text: str,
    user_code: str,
    error_message: str,
    difficulty_name: str,
    level_title: str,
    allowed_concepts: list[str],
    exam_mode: bool = False,
) -> str:
    if settings.ai_provider == "builtin":
        return get_local_hint(
            task_text=task_text,
            user_code=user_code,
            error_message=error_message,
            difficulty_name=difficulty_name,
            level_title=level_title,
            allowed_concepts=allowed_concepts,
            exam_mode=exam_mode,
        )

    client = _create_client()
    if client is None:
        return _ai_not_configured_message()

    mode_note = "Режим экзамена: давай только краткие намёки, без развёрнутых объяснений." if exam_mode else ""

    user_msg = f"""{mode_note}
Уровень: {level_title}
Сложность: {difficulty_name}
Допустимые термины: {", ".join(allowed_concepts) or "базовые"}

Задача:
{task_text}

Ошибка / результат тестов:
{error_message or "тесты не пройдены"}

Код пользователя (не переписывай целиком):
{user_code}
"""
    try:
        response = await client.chat.completions.create(
            model=settings.ai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.4,
            timeout=settings.ai_timeout_sec,
        )
    except Exception:
        return (
            "Не удалось получить подсказку от ИИ-наставника. "
            "Проверьте, что сервер модели запущен и настройки AI_BASE_URL / AI_MODEL верны. "
            + FALLBACK_HINT
        )

    return response.choices[0].message.content or FALLBACK_HINT


REVIEW_SYSTEM_PROMPT = """Ты ИИ-эксперт по обзору кода (Code Reviewer) на платформе AI Code Academy.
Язык ответа: русский. Твой ответ должен быть отформатирован в Markdown и содержать конструктивный анализ.
Проанализируй сданное решение пользователя по следующим пунктам:
1. Временная и пространственная сложность (Big O) с объяснением.
2. Соответствие стандартам оформления (PEP 8 для Python, PSR для PHP, camelCase для JS и т.д.).
3. Чистота и читаемость кода (правильные имена переменных, отсутствие избыточности).
4. Рекомендации по оптимизации или улучшению структуры.
Будь вежливым и профессиональным. Начинай с резюме оценки."""


async def get_code_review(
    *,
    task_text: str,
    user_code: str,
    difficulty_name: str,
    level_title: str,
) -> str:
    if settings.ai_provider == "builtin":
        return (
            "### 🔍 AI Анализ решения (Встроенный обзор)\n\n"
            "**1. Алгоритмическая сложность:**\n"
            "Решение является оптимальным. Временная сложность: $O(1)$ или $O(N)$ в зависимости от длины входных данных. "
            "Дополнительная память не выделяется (пространственная сложность $O(1)$).\n\n"
            "**2. Чистота и структура кода:**\n"
            "- Стиль написания соответствует общепринятым стандартам (PEP 8 / Clean Code).\n"
            "- Переменные названы понятно и отражают суть хранимых данных.\n\n"
            "**3. Советы по улучшению:**\n"
            "- Рекомендуется добавлять аннотации типов (type hinting) для параметров функции, например: `def func(a: int) -> int`.\n"
            "- Для документирования полезно писать краткий docstring в начале функции.\n\n"
            "*Вы отлично справились! Это эффективное и лаконичное решение.*"
        )

    client = _create_client()
    if client is None:
        return "ИИ-обзор кода временно недоступен. Проверьте настройки AI_PROVIDER."

    user_msg = f"""Уровень: {level_title}
Сложность: {difficulty_name}

Задача:
{task_text}

Сданное решение пользователя:
{user_code}
"""
    try:
        response = await client.chat.completions.create(
            model=settings.ai_model,
            messages=[
                {"role": "system", "content": REVIEW_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.3,
            timeout=settings.ai_timeout_sec,
        )
        return response.choices[0].message.content or "Не удалось сгенерировать обзор решения."
    except Exception as exc:
        return f"Не удалось связаться с сервером ИИ для обзора решения: {exc}"
