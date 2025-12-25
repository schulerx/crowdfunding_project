from app.schemes.rewards import SRewardAdd
from app.services.base import BaseService


class RewardsService(BaseService):
    async def get_filtered_rewards(self, offset: int, limit: int,user_id: int | None = None, category_id: int | None = None):
        return await self.db.rewards.get_filtered(offset=offset, limit=limit,user_id=user_id, category_id=category_id)
    
    async def get_reward(self,reward_id: int):
        return await self.db.rewards.get_one_or_none(id=reward_id)
    async def create_reward(self, reward_data: SRewardAdd):
        reward = await self.db.rewards.add(reward_data)
        await self.db.commit()

        return reward