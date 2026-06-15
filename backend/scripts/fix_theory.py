import asyncio
import os
import sys

# Add the parent directory to the system path to allow importing from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine

async def fix():
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        generic_ru = "### 📖 Лекция к задаче\n\nВ этом уроке закрепляются навыки решения задач."
        generic_en = "### 📖 Lecture for the Task\n\nThis lesson consolidates practical skills."
        generic_kz = "### 📖 Тапсырмаға дәріс\n\nБұл сабақта практикалық есеп шешу дағдылары бекітіледі."
        await conn.execute(text(
            "UPDATE levels SET theory_ru = :ru, theory_en = :en, theory_kz = :kz "
            "WHERE (theory_ru IS NULL OR theory_ru = '')"
        ), {"ru": generic_ru, "en": generic_en, "kz": generic_kz})
        print("Fixed theories!")

if __name__ == "__main__":
    asyncio.run(fix())
