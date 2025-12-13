from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.users import SUserGet
    from app.schemes.categories import SCategoriesGet
    from app.schemes.donations import SDonationGet
    from app.schemes.rewards import SRewardGet


class SProjectAdd(BaseModel):
    creator_id: int
    title: str
    description: str
    target_amount: str
    collected_amount: str
    category_id: int
    date_start: int
    date_end: int
    is_active: bool = True


class SProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    target_amount: str | None = None
    collected_amount: str | None = None
    category_id: int | None = None
    date_start: int | None = None
    date_end: int | None = None
    is_active: bool | None = None


class SProjectGet(SProjectAdd):
    id: int


class SProjectsWithRelations(SProjectGet):
    creator: "SUserGet"
    category: "SCategoriesGet"
    donations: list["SDonationGet"] | None = None
    rewards: list["SRewardGet"] | None = None
