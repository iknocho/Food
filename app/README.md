# FastAPI 식품 영양 정보 API

이 프로젝트는 FastAPI 기반의 식품 영양 정보 관리 API입니다.

## 로컬 개발 환경 실행 방법

### 1. Docker 이미지 빌드 및 컨테이너 실행

```bash
docker-compose up --build
```

### 2. API 문서 접속

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. 환경 변수 설정

`.env` 파일을 프로젝트 루트(app)에 위치시키고, 데이터베이스 등 환경변수를 설정하세요.

### 4. 주요 명령어

- 컨테이너 중지: `docker-compose down`
- 로그 확인: `docker-compose logs -f web`

## 개발 관련 참고
- 코드 변경 시 컨테이너가 자동으로 reload 됩니다.
- 데이터베이스 등 추가 서비스가 필요하다면 docker-compose.yaml에 정의하세요. 