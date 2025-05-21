from typing import AsyncGenerator
from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.dependencies import SessionDep
from .models import Food
from src.food.exceptions import FoodNotFoundException

async def get_food_by_id(food_id: UUID, db: SessionDep) -> Food:
    """ID로 식품 정보를 조회하는 의존성 함수"""
    query = select(Food).where(Food.uid == food_id)
    result = await db.execute(query)
    food = result.scalar_one_or_none()
    if not food:
        raise FoodNotFoundException(food_id)
    return food