"""Встроенный ИИ-наставник платформы (без внешнего API).

Анализирует ошибки и даёт сократовские подсказки на русском,
не раскрывая готовое решение.
"""

from __future__ import annotations

import re


def _normalize(text: str) -> str:
    return text.strip().lower()


def _mentions_concept(concepts: list[str], *keywords: str) -> bool:
    lowered = {c.lower() for c in concepts}
    return any(k in lowered for k in keywords)


def _pick_hint(candidates: list[str], exam_mode: bool) -> str:
    if not candidates:
        return (
            "Что именно должна вернуть ваша функция при данных входных значениях? "
            "Попробуйте пройти по шагам на бумаге, прежде чем менять код."
        )
    text = candidates[0] if exam_mode else candidates[0]
    if exam_mode and len(text) > 120:
        return text[:117] + "..."
    return text


def get_local_hint(
    *,
    task_text: str,
    user_code: str,
    error_message: str,
    difficulty_name: str,
    level_title: str,
    allowed_concepts: list[str],
    exam_mode: bool = False,
) -> str:
    err = _normalize(error_message)
    code = user_code or ""
    task = _normalize(task_text)
    hints: list[str] = []

    if "sum_two" in task or "sum_two" in code:
        hints.extend(_sum_two_hints(err, code, allowed_concepts))

    # General Socratic guidance for confused users
    if any(k in err or k in code.lower() for k in ["не знаю", "запутался", "помогите", "что делать", "как решить", "не понимаю", "сложно", "хелп"]):
        hints.append(
            "Не беспокойтесь! Программирование — это разбиение большой задачи на мелкие шаги. "
            f"Для этого уровня разрешены понятия: {', '.join(allowed_concepts) or 'базовые'}. "
            "Давайте начнем с объявления функции и простейшего возврата (например, return 0). Вы увидите результаты тестов и мы продолжим!"
        )

    if ("pass" in code and "return" in err) or "none" in err or "nonetype" in err:
        hints.append(
            "Функция завершилась без значения. Что должно произойти в последней строке тела функции, "
            "чтобы результат дошёл до вызывающего кода?"
        )

    if "syntaxerror" in err or "invalid syntax" in err:
        hints.append(
            "Синтаксическая ошибка часто связана с отступами, скобками или двоеточием после заголовка блока. "
            "Сравните структуру своего кода с примером из условия — где расходится форма?"
        )

    if "nameerror" in err or "is not defined" in err:
        hints.append(
            "Используется имя, которое Python пока не знает. Это имя параметра, локальная переменная "
            "или опечатка в уже объявленном идентификаторе?"
        )

    if "typeerror" in err:
        hints.append(
            "Типы операндов не сходятся с ожидаемой операцией. Какие типы у входных данных "
            "и что именно вы с ними делаете?"
        )

    if "assertionerror" in err or "тест" in err or "expected" in err or "не пройден" in err:
        hints.append(
            "Тест ожидал другое значение. Подставьте вручную аргументы из условия: "
            "какой результат вы получаете сейчас и какой должен быть?"
        )

    if "indentationerror" in err:
        hints.append(
            "Отступы в Python задают вложенность блоков. Все строки внутри функции выровнены одинаково "
            "относительно её объявления?"
        )

    if _mentions_concept(allowed_concepts, "цикл") and ("for" not in code and "while" not in code):
        hints.append(
            "Задача может требовать повторения действия. Есть ли в условии формулировки вроде "
            "«для каждого», «пока» или «перебрать»?"
        )

    if _mentions_concept(allowed_concepts, "условие") and "if " not in code:
        hints.append(
            "Возможно, нужна развилка: разные входные данные требуют разной логики. "
            "При каких случаях поведение функции должно отличаться?"
        )

    if _mentions_concept(allowed_concepts, "список") and "[" not in code:
        hints.append(
            "Работа со списком обычно начинается с понимания, что в нём хранится и как пройти по элементам. "
            "Что является одним элементом в вашей задаче?"
        )

    if not hints:
        hints.append(
            f"Уровень «{level_title}» ({difficulty_name}). "
            "Разбейте задачу на вход, преобразование и выход. "
            "Какой из этих шагов сейчас не реализован в коде?"
        )

    return _pick_hint(hints, exam_mode)


def _sum_two_hints(err: str, code: str, concepts: list[str]) -> list[str]:
    hints: list[str] = []

    if "pass" in code:
        hints.append(
            "В теле функции остался заглушечный pass. Какое выражение с двумя параметрами "
            "даст сумму, если использовать только return?"
        )

    if "print" in code and "return" not in code:
        hints.append(
            "print выводит текст в консоль, но тест проверяет возвращаемое значение функции. "
            "Чем отличается «показать результат» от «вернуть результат»?"
        )

    if re.search(r"\+\s*['\"]", code) or re.search(r"['\"].*\+", code):
        hints.append(
            "Сложение строк и сложение чисел в Python — разные операции. "
            "Какой тип данных ожидается у параметров a и b?"
        )

    if "return" in concepts or _mentions_concept(concepts, "return", "функция"):
        hints.append(
            "Функция sum_two принимает два аргумента. Какое арифметическое действие "
            "превращает пару чисел в их сумму?"
        )

    if not hints:
        hints.append(
            "Подставьте конкретные числа из условия: что вернёт функция сейчас и что должна вернуть?"
        )

    return hints
