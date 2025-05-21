from uuid import UUID
from fastapi import HTTPException, status
from src.food.constants import FOOD_NOT_FOUND, INVALID_FOOD_DATA


class FoodNotFoundException(HTTPException):
    def __init__(self, food_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=FOOD_NOT_FOUND.format(food_id),
        )


class InvalidFoodDataException(HTTPException):
    def __init__(self, detail: str = INVALID_FOOD_DATA):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class FoodSearchConditionRequiredException(Exception):
    def __init__(self):
        super().__init__("최소 1개 이상의 검색 조건이 필요합니다.")