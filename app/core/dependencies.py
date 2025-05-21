from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import async_session
from fastapi import Depends, HTTPException, status


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
        
SessionDep = Annotated[AsyncSession, Depends(get_db)]
