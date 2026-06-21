from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.auth import CurrentAdmin
from app.database import get_db
from app.models import Language
from app.schemas import LanguageOut, LanguageCreate

router = APIRouter(prefix="/languages", tags=["languages"])

@router.get("", response_model=list[LanguageOut])
async def list_languages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language).order_by(Language.id))
    return result.scalars().all()

@router.post("", response_model=LanguageOut)
async def create_language(
    body: LanguageCreate,
    admin: CurrentAdmin,
    db: AsyncSession = Depends(get_db),
):
    lang = Language(code=body.code, name=body.name)
    db.add(lang)
    try:
        await db.commit()
        await db.refresh(lang)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Language with this code already exists")
    
    return lang
