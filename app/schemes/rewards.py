from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.projects import SProjectGet


class SRewardAdd(BaseModel):
    project_id: int | None = None
    title: str | None = None
    description: str | None = None
    required_quantity: int | None = None


class SRewardUpdate(BaseModel):
    project_id: int | None = None
    title: str | None = None
    description: str | None = None
    required_quantity: int | None = None


class SRewardGet(SRewardAdd):
    id: int


class SRewardWithProject(SRewardGet):
    project: "SProjectGet" | None = None