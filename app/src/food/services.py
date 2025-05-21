from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, func

from src.food.models import Food
from src.food.schemas import FoodCreate, FoodUpdate
from src.food.exceptions import FoodNotFoundException
from src.food.utils import paginate_query


async def create_food(db: AsyncSession, food_data: FoodCreate) -> Food:
    """식품 정보 생성"""
    food = Food(**food_data.model_dump())
    db.add(food)
    await db.commit()
    await db.refresh(food)
    return food


async def get_food(db: AsyncSession, food_id: UUID) -> Food:
    """단일 식품 정보 조회"""
    query = select(Food).where(Food.uid == food_id)
    result = await db.execute(query)
    food = result.scalar_one_or_none()
    if not food:
        raise FoodNotFoundException(food_id)
    return food


async def get_foods(
    db: AsyncSession, 
    food_name: Optional[str] = None,
    research_year: Optional[int] = None,
    maker_name: Optional[str] = None,
    food_code: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100,
) -> Dict[str, Any]:
    """식품 정보 목록 조회 및 필터링"""
    query = select(Food)
    
    # 필터 조건 적용
    if food_name:
        query = query.where(Food.food_name.ilike(f"%{food_name}%"))
    if research_year:
        query = query.where(Food.research_year == research_year)
    if maker_name:
        query = query.where(Food.maker_name.ilike(f"%{maker_name}%"))
    if food_code:
        query = query.where(Food.food_code == food_code)
    
    # 페이지네이션 유틸 사용
    return await paginate_query(db, query, skip=skip, limit=limit)

async def update_food(db: AsyncSession, food_id: UUID, food_data: FoodUpdate) -> Food:
    """식품 정보 수정"""
    query = select(Food).where(Food.uid == food_id)
    result = await db.execute(query)
    food = result.scalar_one_or_none()
    
    if not food:
        raise FoodNotFoundException(food_id)
    
    update_data = food_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(food, key, value)
    
    await db.commit()
    await db.refresh(food)
    return food


async def delete_food(db: AsyncSession, food_id: UUID) -> None:
    """식품 정보 삭제"""
    query = select(Food).where(Food.uid == food_id)
    result = await db.execute(query)
    food = result.scalar_one_or_none()
    
    if not food:
        raise FoodNotFoundException(food_id)
    
    await db.delete(food)
    await db.commit()