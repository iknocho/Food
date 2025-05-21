from fastapi.middleware.cors import CORSMiddleware  # CORS 추가
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging.config
import logging
from src.food.models import Food
from core.database import engine, Base
from src.food.router import router as foods_router
from utils import init_db
# 로깅 설정
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# 시작 시 데이터베이스 초기화 함수
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 테이블 생성 (필요한 경우)
    async with engine.begin() as conn:
        # 개발 환경에서만 사용 (프로덕션에서는 마이그레이션 도구 사용)
        # await conn.run_sync(Base.metadata.drop_all)  
        await conn.run_sync(Base.metadata.create_all)
    logger.info("데이터베이스 테이블 초기화 완료")
    # 초기 데이터 초기화
    await init_db()
    yield
    # 종료 시 작업
    logger.info("애플리케이션 종료")

app = FastAPI(
    title="식품 영양 정보 API",
    description="식품 영양 정보를 관리하는 비동기 API",
    version="1.0.0",
    lifespan=lifespan
)

# 라우터 포함
app.include_router(foods_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #http://localhost:3000","https://45d8-183-100-236-188.ngrok-free.app React 앱이 실행되는 도메인
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

from sqladmin import Admin, ModelView
admin = Admin(app, engine, base_url="/admin", templates_dir="templates")
class FoodAdmin(ModelView, model=Food):
    column_list = [Food.food_name]

admin.add_view(FoodAdmin)