
"""
Репозиторий
"""
import os
import logging
from typing import Generator, AsyncGenerator
from functools import cached_property

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session


class DatabaseUrlNotSetError(Exception):
    """
    Ошибка путого пути к БД
    """


class DatabaseManager:
    """
    Менеджер подключения к базе данных с поддержкой синхронных и асинхронных сессий.
    """

    def __init__(self, db_url: str | None = None):
        self._db_url = db_url or os.getenv("DATABASE_URL")
        if not self._db_url:
            logging.error("Не задан путь к БД в переменной окружения DATABASE_URL")
            raise DatabaseUrlNotSetError("Не задан путь к БД в переменной окружения DATABASE_URL")

    @cached_property
    def sync_engine(self):
        """Синхронный SQLAlchemy Engine."""
        return create_engine(f"postgresql+psycopg2://{self._db_url}")

    @cached_property
    def async_engine(self):
        """Асинхронный SQLAlchemy Engine."""
        return create_async_engine(f"postgresql+asyncpg://{self._db_url}")

    @cached_property
    def session_local(self):
        """Фабрика синхронных сессий."""
        return sessionmaker(autocommit=False, autoflush=False, bind=self.sync_engine)

    @cached_property
    def async_session_local(self):
        """Фабрика асинхронных сессий."""
        return sessionmaker(self.async_engine, class_=AsyncSession, expire_on_commit=False)

    def get_session(self) -> Generator[Session, None, None]:
        """Генератор синхронной сессии. Использовать через dependency injection в FastAPI."""
        with self.session_local() as session:
            yield session

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Генератор асинхронной сессии."""
        async with self.async_session_local() as session:
            yield session
