from typing import Dict, Any, List, TypeVar, Generic, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.sql.selectable import Select

async def paginate_query(
    db: AsyncSession,
    query: Select,
    skip: int = 0, 
    limit: int = 100
) -> Dict[str, Any]:
    """
    SQLAlchemy 비동기 쿼리 페이지네이션 도우미 함수
    """
    # 총 레코드 수 조회
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # 페이지네이션 적용
    result = await db.execute(query.offset(skip).limit(limit))
    items = result.scalars().all()
    
    return {
        "items": list(items),
        "total": total,
        "skip": skip,
        "limit": limit
    }