import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func, text
from core.database import engine
from src.food.models import Food
import logging

logger = logging.getLogger(__name__)

# 비동기 세션 생성기
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with async_session() as session:
        # 테이블에 데이터가 있는지 확인
        await session.execute(text("LOCK TABLE foods IN ACCESS EXCLUSIVE MODE"))

        count_stmt = select(func.count()).select_from(Food)
        result = await session.execute(count_stmt)
        food_count = result.scalar()

        if food_count == 0:
            logger.info("초기 데이터가 없어 Excel에서 데이터를 삽입합니다.")
            df = pd.read_excel("fooddb_20230715.xlsx", engine="openpyxl")
            # 열 이름 매핑
            df = df.rename(columns={
                "식품코드": "food_code",
                "DB군": "group_name",
                "식품명": "food_name",
                "연도": "research_year",
                "지역 / 제조사": "maker_name",
                "채취시기": "ref_name",
                "1회제공량": "serving_size",
                "에너지(㎉)": "calorie",
                "탄수화물(g)": "carbohydrate",
                "단백질(g)": "protein",
                "지방(g)": "province",
                "총당류(g)": "sugars",
                "나트륨(㎎)": "salt",
                "콜레스테롤(㎎)": "cholesterol",
                "총 포화 지방산(g)": "saturated_fatty_acids",
                "트랜스 지방산(g)": "trans_fat"
            })
            numeric_columns = [
                "serving_size", "calorie", "carbohydrate", "protein", "province",
                "sugars", "salt", "cholesterol", "saturated_fatty_acids", "trans_fat"
            ]
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            # 필요한 열만 필터링
            df = df[[
                "food_code", "group_name", "food_name", "research_year", "maker_name", "ref_name",
                "serving_size", "calorie", "carbohydrate", "protein", "province", "sugars",
                "salt", "cholesterol", "saturated_fatty_acids", "trans_fat"
            ]]
            # NaN → None
            records = df.replace({pd.NA: None}).to_dict(orient="records")
            
            logger.info(records[0])
            
            # 데이터 삽입
            session.add_all([Food(**record) for record in records])
            await session.commit()
            logger.info(f"{len(records)}개의 식품 데이터를 삽입했습니다.")
            
        else:
            logger.info("DB에 이미 데이터가 존재하여 삽입하지 않습니다.")