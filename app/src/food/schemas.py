from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class FoodBase(BaseModel):
    food_code: str = Field(..., description="식품코드")
    group_name: str = Field(..., description="식품군")
    food_name: str = Field(..., description="식품이름")
    research_year: int = Field(..., description="조사년도")
    maker_name: Optional[str] = Field(None, description="지역/제조사")
    ref_name: Optional[str] = Field(None, description="자료출처")
    serving_size: Optional[float] = Field(None, description="1회 제공량")
    calorie: Optional[float] = Field(None, description="열량(kcal)(1회제공량당)")
    carbohydrate: Optional[float] = Field(None, description="탄수화물(g)(1회제공량당)")
    protein: Optional[float] = Field(None, description="단백질(g)(1회제공량당)")
    province: Optional[float] = Field(None, description="지방(g)(1회제공량당)")
    sugars: Optional[float] = Field(None, description="총당류(g)(1회제공량당)")
    salt: Optional[float] = Field(None, description="나트륨(mg)(1회제공량당)")
    cholesterol: Optional[float] = Field(None, description="콜레스테롤(mg)(1회제공량당)")
    saturated_fatty_acids: Optional[float] = Field(None, description="포화지방산(g)(1회제공량당)")
    trans_fat: Optional[float] = Field(None, description="트랜스지방(g)(1회제공량당)")


class FoodCreate(FoodBase):
    pass

class FoodUpdate(BaseModel):
    food_cd: Optional[str] = None
    group_name: Optional[str] = None
    food_name: Optional[str] = None
    research_year: Optional[int] = None
    maker_name: Optional[str] = None
    ref_name: Optional[str] = None
    serving_size: Optional[float] = None
    calorie: Optional[float] = None
    carbohydrate: Optional[float] = None
    protein: Optional[float] = None
    province: Optional[float] = None
    sugars: Optional[float] = None
    salt: Optional[float] = None
    cholesterol: Optional[float] = None
    saturated_fatty_acids: Optional[float] = None
    trans_fat: Optional[float] = None


class Link(BaseModel):
    rel: str
    href: str


class FoodResponse(FoodBase):
    uid: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    links: Optional[List[Link]] = None

    # Pydantic v2에서는 class Config 대신 model_config 사용
    model_config = ConfigDict(from_attributes=True)


class FoodListResponse(BaseModel):
    items: List[FoodResponse]
    total: int
    links: Optional[List[Link]] = None