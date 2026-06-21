import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

database_url = 'postgresql+asyncpg://postgres:123456@localhost:5432/ai_academy_1'
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("DATABASE_URL="):
                database_url = line.strip().split("DATABASE_URL=")[1].strip()

async def main():
    engine = create_async_engine(database_url, echo=False)
    async with engine.begin() as conn:
        await conn.execute(text("INSERT INTO languages (id, code, name) VALUES (6, 'cpp', 'C++') ON CONFLICT (id) DO NOTHING"))
        print('C++ language added with ID 6.')

if __name__ == "__main__":
    asyncio.run(main())
