import uuid
from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from core.database import Base

class Food(Base):
    __tablename__ = "foods"

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    food_code = Column(String(255), nullable=False, index=True)
    group_name = Column(String(255), nullable=False)
    food_name = Column(String(255), nullable=False, index=True)
    research_year = Column(Integer, nullable=False, index=True)
    maker_name = Column(String(255), nullable=True, index=True)
    ref_name = Column(String(255), nullable=True)
    serving_size = Column(Float, nullable=True)
    calorie = Column(Float, nullable=True)
    carbohydrate = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    province = Column(Float, nullable=True)
    sugars = Column(Float, nullable=True)
    salt = Column(Float, nullable=True)
    cholesterol = Column(Float, nullable=True)
    saturated_fatty_acids = Column(Float, nullable=True)
    trans_fat = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())