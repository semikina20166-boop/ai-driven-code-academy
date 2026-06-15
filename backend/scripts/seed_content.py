import asyncio
import os
import sys

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the system path to allow importing from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.models import Level, Track, Difficulty, Language

engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Templates for each language and difficulty
CONTENT_TEMPLATES = {
    "python": {
        "easy": {
            "title_ru": "Базовые операции и функции",
            "title_en": "Basic Operations and Functions",
            "title_kz": "Негізгі амалдар және функциялар",
            "task_ru": "Реализуйте функцию solve(a, b), возвращающую сумму.",
            "task_en": "Implement the solve(a, b) function returning the sum.",
            "task_kz": "solve(a, b) функциясын іске асырыңыз, қосындысын қайтарады.",
            "code": "def solve(a, b):\n    # ваш код\n    pass\n",
            "tests": {"function": "solve", "language": "python", "cases": [{"args": [2, 3], "expected": 5}, {"args": [-1, 1], "expected": 0}]}
        },
        "medium": {
            "title_ru": "Циклы и списки",
            "title_en": "Loops and Lists",
            "title_kz": "Циклдер мен тізімдер",
            "task_ru": "Реализуйте функцию solve(arr), возвращающую сумму элементов списка.",
            "task_en": "Implement the solve(arr) function returning the sum of the list elements.",
            "task_kz": "solve(arr) функциясын іске асырыңыз, тізім элементтерінің қосындысын қайтарады.",
            "code": "def solve(arr):\n    # ваш код\n    pass\n",
            "tests": {"function": "solve", "language": "python", "cases": [{"args": [[1, 2, 3]], "expected": 6}, {"args": [[]], "expected": 0}]}
        },
        "hard": {
            "title_ru": "Алгоритмы сортировки",
            "title_en": "Sorting Algorithms",
            "title_kz": "Сұрыптау алгоритмдері",
            "task_ru": "Реализуйте функцию solve(arr), возвращающую отсортированный массив.",
            "task_en": "Implement the solve(arr) function returning the sorted array.",
            "task_kz": "solve(arr) функциясын іске асырыңыз, сұрыпталған массивті қайтарады.",
            "code": "def solve(arr):\n    # ваш код\n    pass\n",
            "tests": {"function": "solve", "language": "python", "cases": [{"args": [[3, 1, 2]], "expected": [1, 2, 3]}]}
        }
    },
    "javascript": {
        "easy": {
            "title_ru": "Базовые операции",
            "title_en": "Basic Operations",
            "title_kz": "Негізгі амалдар",
            "task_ru": "Реализуйте функцию solve(a, b), возвращающую сумму.",
            "task_en": "Implement the solve(a, b) function returning the sum.",
            "task_kz": "solve(a, b) функциясын іске асырыңыз, қосындысын қайтарады.",
            "code": "function solve(a, b) {\n    // ваш код\n}\nmodule.exports = { solve };",
            "tests": {"function": "solve", "language": "javascript", "cases": [{"args": [2, 3], "expected": 5}, {"args": [-1, 1], "expected": 0}]}
        },
        "medium": {
            "title_ru": "Массивы и объекты",
            "title_en": "Arrays and Objects",
            "title_kz": "Массивтер мен нысандар",
            "task_ru": "Реализуйте функцию solve(arr), возвращающую длину массива.",
            "task_en": "Implement the solve(arr) function returning the length of the array.",
            "task_kz": "solve(arr) функциясын іске асырыңыз, массив ұзындығын қайтарады.",
            "code": "function solve(arr) {\n    // ваш код\n}\nmodule.exports = { solve };",
            "tests": {"function": "solve", "language": "javascript", "cases": [{"args": [[1, 2, 3]], "expected": 3}, {"args": [[]], "expected": 0}]}
        },
        "hard": {
            "title_ru": "Асинхронность",
            "title_en": "Asynchrony",
            "title_kz": "Асинхрондылық",
            "task_ru": "Реализуйте функцию solve(x), возвращающую x * 2.",
            "task_en": "Implement the solve(x) function returning x * 2.",
            "task_kz": "solve(x) функциясын іске асырыңыз, x * 2 қайтарады.",
            "code": "function solve(x) {\n    return x * 2;\n}\nmodule.exports = { solve };",
            "tests": {"function": "solve", "language": "javascript", "cases": [{"args": [5], "expected": 10}]}
        }
    }
}

async def run():
    async with AsyncSessionLocal() as session:
        # Load all levels with related track, difficulty, language
        result = await session.execute(
            select(Level)
            .join(Level.track)
            .join(Track.language)
            .join(Level.difficulty)
        )
        levels = result.scalars().all()
        
        updated = 0
        for lvl in levels:
            await session.refresh(lvl, ['track', 'difficulty'])
            await session.refresh(lvl.track, ['language'])
            lang_code = lvl.track.language.code
            diff_code = lvl.difficulty.code
            num = lvl.order_num
            
            # Use specific template if exists, else fallback to python templates
            tpl_lang = CONTENT_TEMPLATES.get(lang_code, CONTENT_TEMPLATES["python"])
            tpl = tpl_lang.get(diff_code)
            
            if tpl:
                lvl.title_ru = f"Урок {num}: {tpl['title_ru']}"
                lvl.title_en = f"Lesson {num}: {tpl['title_en']}"
                lvl.title_kz = f"Сабақ {num}: {tpl['title_kz']}"
                
                lvl.task_text_ru = f"Задача {num}.\n\n{tpl['task_ru']}"
                lvl.task_text_en = f"Task {num}.\n\n{tpl['task_en']}"
                lvl.task_text_kz = f"Тапсырма {num}.\n\n{tpl['task_kz']}"
                
                lvl.starter_code = tpl['code']
                
                # Fix language code in tests if fallback was used
                tests = tpl['tests'].copy()
                tests['language'] = lang_code
                lvl.solution_tests = tests
                
                updated += 1

        await session.commit()
        print(f"Успешно обновлено {updated} уровней!")

if __name__ == "__main__":
    asyncio.run(run())
