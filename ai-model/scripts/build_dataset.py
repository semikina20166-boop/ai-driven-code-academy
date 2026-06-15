"""Сборка датасета для обучения ИИ-наставника.

Источники:
  - data/training_examples.json  — основной набор (задача, код, ошибка, подсказка)
  - data/seed_examples.jsonl     — дополнительные примеры вручную
  - встроенные TEMPLATE_EXAMPLES

Запуск: python scripts/build_dataset.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SEED_PATH = DATA_DIR / "seed_examples.jsonl"
TRAINING_PATH = DATA_DIR / "training_examples.json"
OUT_PATH = DATA_DIR / "train.jsonl"

SYSTEM_PROMPT = (DATA_DIR / "system_prompt.txt").read_text(encoding="utf-8").strip()


def user_message(
    *,
    level_title: str,
    difficulty_name: str,
    allowed_concepts: list[str],
    task_text: str,
    error_message: str,
    user_code: str,
    exam_mode: bool = False,
) -> str:
    mode_note = "Режим экзамена: давай только краткие намёки, без развёрнутых объяснений." if exam_mode else ""
    return f"""{mode_note}
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


def example(task_text: str, user_code: str, error: str, hint: str, **meta: str | list[str] | bool) -> dict:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": user_message(
                    level_title=str(meta.get("level_title", "Python / Начальный — уровень 1")),
                    difficulty_name=str(meta.get("difficulty_name", "Начальный")),
                    allowed_concepts=list(meta.get("allowed_concepts", ["переменная", "функция", "return"])),
                    task_text=task_text,
                    error_message=error,
                    user_code=user_code,
                    exam_mode=bool(meta.get("exam_mode", False)),
                ),
            },
            {"role": "assistant", "content": hint},
        ]
    }


def load_training_json() -> list[dict]:
    if not TRAINING_PATH.exists():
        return []
    rows = json.loads(TRAINING_PATH.read_text(encoding="utf-8"))
    return [
        example(
            row["task_text"],
            row["user_code"],
            row["error"],
            row["hint"],
            level_title=row.get("level_title", "Python / Начальный — уровень 1"),
            difficulty_name=row.get("difficulty_name", "Начальный"),
            allowed_concepts=row.get("allowed_concepts", ["переменная", "функция", "return"]),
            exam_mode=row.get("exam_mode", False),
        )
        for row in rows
    ]


def load_seed() -> list[dict]:
    if not SEED_PATH.exists():
        return []
    rows: list[dict] = []
    for line in SEED_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def main() -> None:
    rows = load_seed() + load_training_json()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Сохранено {len(rows)} примеров в {OUT_PATH}")


if __name__ == "__main__":
    main()
