from fastapi import APIRouter, Depends, HTTPException

from typing import List, Optional
from app.api.dependencies import DBDep
from app.models.rewards import RewardModel
from app.schemes.rewards import SRewardAdd, SRewardUpdate, SRewardGet

router = APIRouter(prefix="/api/rewards", tags=["rewards"])

@router.get("/", response_model=List[SRewardGet])
async def get_rewards(
    db: DBDep,
    skip: int = 0, 
    limit: int = 100, 
    project_id: Optional[int] = None,
   
):
    """Получить все награды с фильтрацией"""
    query = db.query(RewardModel)
    
    if project_id:
        query = query.filter(RewardModel.project_id == project_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{reward_id}", response_model=SRewardGet)
async def get_reward(db: DBDep, reward_id: int):
    """Получить награду по ID"""
    reward = db.query(RewardModel).filter(RewardModel.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Награда не найдена")
    return reward

@router.post("/", response_model=SRewardGet, status_code=201)
async def create_reward(db: DBDep,reward_data: SRewardAdd):
    """Создать новую награду"""
    reward = RewardModel(**reward_data.dict())
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward

@router.put("/{reward_id}", response_model=SRewardGet)
async def update_reward(
    db: DBDep,
    reward_id: int, 
    reward_data: SRewardUpdate, 
 
):
    """Обновить награду"""
    reward = db.query(RewardModel).filter(RewardModel.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Награда не найдена")
    
    for key, value in reward_data.dict(exclude_unset=True).items():
        setattr(reward, key, value)
    
    db.commit()
    db.refresh(reward)
    return reward

@router.delete("/{reward_id}")
async def delete_reward(db: DBDep, reward_id: int):
    """Удалить награду"""
    reward = db.query(RewardModel).filter(RewardModel.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Награда не найдена")
    
    db.delete(reward)
    db.commit()
    return {"message": "Награда успешно удалена"}