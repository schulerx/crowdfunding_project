from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.rewards import RewardModel
from app.repositories.base import BaseRepository
from app.schemes.rewards import SRewardGet


class RewardsRepository(BaseRepository):
    model = RewardModel
    schema = SRewardGet