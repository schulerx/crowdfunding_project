



from app.schemes.projects import SProjectAdd
from app.services.base import BaseService


class ProjectsService(BaseService):
    async def get_filtered_projects(self, offset: int, limit: int,user_id: int | None, category_id: int | None):
        return await self.db.projects.get_filtered(offset=offset, limit=limit,user_id=user_id, category_id=category_id)
    
    async def get_project(self,project_id: int):
        return await self.db.projects.get_one_or_none(id=project_id)
    async def create_project(self, project_data: SProjectAdd):
        project = await self.db.projects.add(project_data)
        await self.db.commit()

        return project