from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.projects import SProjectGet


class SCategoriesAdd(BaseModel):
    name: str


class SCategoriesUpdate(BaseModel):
    name: str | None = None


class SCategoriesGet(SCategoriesAdd):
    id: int


class SCategoriesWithProjects(SCategoriesGet):
    projects: list["SProjectGet"] | None = None