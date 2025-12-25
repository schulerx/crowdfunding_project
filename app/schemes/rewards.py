
from pydantic import BaseModel




class SRewardAdd(BaseModel):
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
