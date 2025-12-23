from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import async_session_maker
from app.database.repositories.base import BaseRepository


class DBManager:
    def __init__(self, session_factory=async_session_maker):
        self.session_factory = session_factory
        self.session: AsyncSession = None
        self._repositories: Dict[str, BaseRepository] = {}
    
    async def __aenter__(self):
        self.session = self.session_factory()
        await self._initialize_repositories()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise
        finally:
            await self.session.close()
    
    async def _initialize_repositories(self):
        """Динамическая инициализация всех репозиториев"""
        from app.database.repositories import (
            UsersRepository, RolesRepository, ProjectsRepository,
            CategoriesRepository, DonationsRepository, RewardsRepository
        )
        
        repo_classes = {
            'users': UsersRepository,
            'roles': RolesRepository,
            'projects': ProjectsRepository,
            'categories': CategoriesRepository,
            'donations': DonationsRepository,
            'rewards': RewardsRepository,
        }
        
        for name, repo_class in repo_classes.items():
            setattr(self, name, repo_class(self.session))
            self._repositories[name] = getattr(self, name)
    
    def get_repository(self, name: str) -> BaseRepository:
        """Получить репозиторий по имени"""
        return self._repositories.get(name)
    
    async def commit(self):
        """Явный коммит транзакции"""
        await self.session.commit()
    
    async def rollback(self):
        """Явный откат транзакции"""
        await self.session.rollback()


@asynccontextmanager
async def get_db_manager() -> AsyncGenerator[DBManager, None]:
    """Асинхронный контекстный менеджер для DBManager"""
    async with DBManager() as db:
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
