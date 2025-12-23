from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.project import ProjectModel
from app.repositories.base import BaseRepository
from app.schemes.projects import SProjectGet


class ProjectsRepository(BaseRepository):
    model = ProjectModel
    schema = SProjectGet