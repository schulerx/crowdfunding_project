from typing import Type, TypeVar, Optional, List, Dict, Any, Union
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.database.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository:
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def create(self, **kwargs) -> ModelType:
        """Создание новой записи"""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance
    
    async def get(self, id: int) -> Optional[ModelType]:
        """Получение записи по ID"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_one_or_none(self, **filters) -> Optional[ModelType]:
        """Получение одной записи или None"""
        query = select(self.model)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        **filters
    ) -> List[ModelType]:
        """Получение всех записей с фильтрацией"""
        query = select(self.model)
        
        # Применяем фильтры
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
        
        # Пагинация
        query = query.offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Обновление записи"""
        # Получаем запись
        instance = await self.get(id)
        if not instance:
            return None
        
        # Обновляем поля
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        await self.session.flush()
        return instance
    
    async def delete(self, id: int) -> bool:
        """Удаление записи"""
        instance = await self.get(id)
        if not instance:
            return False
        
        await self.session.delete(instance)
        await self.session.flush()
        return True
    
    async def count(self, **filters) -> int:
        """Подсчет количества записей"""
        query = select(func.count()).select_from(self.model)
        
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
        
        result = await self.session.execute(query)
        return result.scalar()
    
    async def exists(self, **filters) -> bool:
        """Проверка существования записи"""
        return await self.count(**filters) > 0


class BaseRepositoryWithRelations(BaseRepository):
    """Базовый репозиторий для моделей с отношениями"""
    
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        super().__init__(model, session)
        self._relation_options = []
    
    def add_relation_option(self, option):
        """Добавление опций для загрузки отношений"""
        self._relation_options.append(option)
        return self
    
    async def get_with_relations(self, id: int) -> Optional[ModelType]:
        """Получение записи с загруженными отношениями"""
        query = select(self.model).where(self.model.id == id)
        
        for option in self._relation_options:
            query = query.options(option)
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
