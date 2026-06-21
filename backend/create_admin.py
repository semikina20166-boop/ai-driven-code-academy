import asyncio
import os
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.auth import hash_password

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

database_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_academy"
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("DATABASE_URL="):
                database_url = line.strip().split("DATABASE_URL=")[1].strip()

async def main():
    engine = create_async_engine(database_url, echo=False)
    
    try:
        async with engine.begin() as conn:
            print("Checking if is_admin column exists...")
            await conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;"))
            print("Added is_admin column.")
    except Exception as e:
        print("Column is_admin likely already exists.")
        
    async with engine.begin() as conn:
        print("Creating or updating admin user...")
        # Check if admin exists
        result = await conn.execute(text("SELECT id FROM users WHERE email = 'admin@gmail.com'"))
        admin_id = result.scalar_one_or_none()
        
        hashed_pw = hash_password("123admin")
        
        if admin_id:
            await conn.execute(text(
                "UPDATE users SET is_admin = TRUE, password_hash = :pw, display_name = 'admin' WHERE id = :id"
            ), {"pw": hashed_pw, "id": admin_id})
            print("Admin user updated.")
        else:
            await conn.execute(text(
                "INSERT INTO users (email, password_hash, display_name, is_admin) "
                "VALUES ('admin@gmail.com', :pw, 'admin', TRUE)"
            ), {"pw": hashed_pw})
            print("Admin user created.")

if __name__ == "__main__":
    asyncio.run(main())
