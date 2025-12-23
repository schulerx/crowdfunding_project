from sqlalchemy.orm import selectinload
from app.database.repositories.base import BaseRepositoryWithRelations
from app.database.models.role import RoleModel


class RolesRepository(BaseRepositoryWithRelations):
    def __init__(self, session):
        super().__init__(RoleModel, session)
        # Добавляем загрузку пользователей для роли
        self.add_relation_option(selectinload(RoleModel.users))
    
    async def get_by_name(self, name: str):
        """Получение роли по имени"""
        return await self.get_one_or_none(name=name)
    
    async def get_role_with_users(self, role_id: int):
        """Получение роли с пользователями"""
        return await self.get_with_relations(role_id)
    
    async def get_all_with_user_count(self, skip: int = 0, limit: int = 100):
        """Получение всех ролей с количеством пользователей"""
        from sqlalchemy import func
        
        query = (
            select(
                RoleModel,
                func.count(RoleModel.users).label('user_count')
            )
            .join(RoleModel.users, isouter=True)
            .group_by(RoleModel.id)
            .offset(skip)
            .limit(limit)
        )
        
        result = await self.session.execute(query)
        return result.all()
