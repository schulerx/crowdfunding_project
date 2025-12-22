from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.reward import Reward
from app.schemas.reward import RewardCreate, RewardUpdate, RewardResponse

router = APIRouter(prefix="/api/rewards", tags=["rewards"])

@router.get("/", response_model=List[RewardResponse])
async def get_rewards(
    skip: int = 0, 
    limit: int = 100, 
    project_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Получить все награды с фильтрацией"""
    query = db.query(Reward)
    
    if project_id:
        query = query.filter(Reward.project_id == project_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{reward_id}", response_model=RewardResponse)
async def get_reward(reward_id: int, db: Session = Depends(get_db)):
    """Получить награду по ID"""
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Награда не найдена")
    return reward

@router.post("/", response_model=RewardResponse, status_code=201)
async def create_reward(reward_data: RewardCreate, db: Session = Depends(get_db)):
    """Создать новую награду"""
    reward = Reward(**reward_data.dict())
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward

@router.put("/{reward_id}", response_model=RewardResponse)
async def update_reward(
    reward_id: int, 
    reward_data: RewardUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить награду"""
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Награда не найдена")
    
    for key, value in reward_data.dict(exclude_unset=True).items():
        setattr(reward, key, value)
    
    db.commit()
    db.refresh(reward)
    return reward

@router.delete("/{reward_id}")
async def delete_reward(reward_id: int, db: Session = Depends(get_db)):
    """Удалить награду"""
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Награда не найдена")
    
    db.delete(reward)
    db.commit()
    return {"message": "Награда успешно удалена"}