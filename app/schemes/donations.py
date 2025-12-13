from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.users import SUserGet
    from app.schemes.projects import SProjectGet


class SDonationAdd(BaseModel):
    project_id: int
    user_id: int
    amount: int


class SDonationUpdate(BaseModel):
    project_id: int | None = None
    user_id: int | None = None
    amount: int | None = None


class SDonationGet(SDonationAdd):
    id: int


class SDonationWithRelations(SDonationGet):
    user: "SUserGet"
    project: "SProjectGet"