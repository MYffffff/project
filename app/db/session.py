from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings


settings = get_settings()
engine = create_async_engine(settings.sqlalchemy_database_uri, echo=False, future=True)
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
