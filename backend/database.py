from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# 데이터베이스 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 사용 전 연결 확인
    echo=True  # SQL 문 로깅 (프로덕션에서는 False)
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 베이스 클래스
Base = declarative_base()


def get_db():
    """데이터베이스 세션 의존성."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
