from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status, Query, Request

from core.dependencies import SessionDep
from src.food.dependencies import get_food_by_id
from src.food.schemas import FoodCreate, FoodResponse, FoodUpdate, FoodListResponse, Link
from src.food.services import create_food, get_foods, update_food, delete_food
from src.food.models import Food

router = APIRouter(prefix="/foods", tags=["foods"])


@router.post(
    "/", 
    response_model=FoodResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="새 식품 정보 생성"
)
async def create_new_food(
    food_data: FoodCreate, 
    db: SessionDep,
    request: Request
):
    """새 식품 정보를 생성합니다"""
    food = await create_food(db, food_data)
    food_response = FoodResponse.model_validate(food)
    food_dict = food_response.model_dump()
    food_id = str(food.uid)
    base_url = str(request.base_url).rstrip("/")
    food_dict["links"] = [
        {"rel": "self", "href": f"{base_url}/foods/{food_id}"},
        {"rel": "update", "href": f"{base_url}/foods/{food_id}"},
        {"rel": "delete", "href": f"{base_url}/foods/{food_id}"}
    ]
    return food_dict


@router.get(
    "/{food_id}", 
    response_model=FoodResponse, 
    summary="ID로 식품 정보 조회"
)
async def get_food_by_id_route(
    request: Request,
    food: Food = Depends(get_food_by_id)
):
    """ID로 식품 정보를 조회합니다"""
    food_response = FoodResponse.model_validate(food)
    food_dict = food_response.model_dump()
    food_id = str(food.uid)
    base_url = str(request.base_url).rstrip("/")
    food_dict["links"] = [
        {"rel": "self", "href": f"{base_url}/foods/{food_id}"},
        {"rel": "update", "href": f"{base_url}/foods/{food_id}"},
        {"rel": "delete", "href": f"{base_url}/foods/{food_id}"}
    ]
    return food_dict


@router.get(
    "/", 
    response_model=FoodListResponse, 
    summary="식품 정보 목록 조회"
)
async def get_all_foods(
    request: Request,
    db: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    food_name: Optional[str] = None,
    research_year: Optional[int] = None,
    maker_name: Optional[str] = None,
    food_code: Optional[str] = None,
):
    """식품 정보를 검색합니다"""
    result = await get_foods(
        db=db,
        food_name=food_name,
        research_year=research_year,
        maker_name=maker_name,
        food_code=food_code,
        skip=skip,
        limit=limit,
    )
    print("결과", result)
    base_url = str(request.base_url).rstrip("/")
    items = []
    for item in result["items"]:
        food_response = FoodResponse.model_validate(item)
        food_dict = food_response.model_dump()
        food_id = str(item.uid)
        food_dict["links"] = [
            {"rel": "self", "href": f"{base_url}/foods/{food_id}"},
            {"rel": "update", "href": f"{base_url}/foods/{food_id}"},
            {"rel": "delete", "href": f"{base_url}/foods/{food_id}"}
        ]
        items.append(food_dict)
    response = {
        "items": items,
        "total": result["total"],
        "links": [
            {"rel": "self", "href": f"{base_url}/foods"}
        ]
    }
    return response


@router.patch(
    "/{food_id}", 
    response_model=FoodResponse, 
    summary="식품 정보 수정"
)
async def update_food_route(
    food_data: FoodUpdate,
    food_id: UUID,
    db: SessionDep,
    request: Request
):
    """식품 정보를 수정합니다"""
    updated_food = await update_food(db, food_id, food_data)
    food_response = FoodResponse.model_validate(updated_food)
    food_dict = food_response.model_dump()
    base_url = str(request.base_url).rstrip("/")
    food_id_str = str(food_id)
    food_dict["links"] = [
        {"rel": "self", "href": f"{base_url}/foods/{food_id_str}"},
        {"rel": "update", "href": f"{base_url}/foods/{food_id_str}"},
        {"rel": "delete", "href": f"{base_url}/foods/{food_id_str}"}
    ]
    return food_dict


@router.delete(
    "/{food_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="식품 정보 삭제"
)
async def delete_food_route(
    food_id: UUID,
    db: SessionDep
):
    """ID로 식품 정보를 삭제합니다"""
    await delete_food(db, food_id)
    return None