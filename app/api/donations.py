from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.dependencies import DBDep
from app.models.donations import DonationModel
from app.schemes.donations import SDonationAdd, SDonationUpdate, SDonationGet

router = APIRouter(prefix="/api/donations", tags=["donations"])

@router.get("/", response_model=List[SDonationGet])
async def get_donations(
    db: DBDep,
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = None,
    project_id: Optional[int] = None,
    
):
    """Получить все пожертвования с фильтрацией"""
    query = db.query(DonationModel)
    
    if user_id:
        query = query.filter(DonationModel.user_id == user_id)
    if project_id:
        query = query.filter(DonationModel.project_id == project_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{donation_id}", response_model=SDonationGet)
async def get_donation(db: DBDep,donation_id: int):
    """Получить пожертвование по ID"""
    donation = db.query(DonationModel).filter(DonationModel.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Пожертвование не найдено")
    return donation

@router.post("/", response_model=SDonationGet, status_code=201)
async def create_donation(db: DBDep, donation_data: SDonationAdd):
    """Создать новое пожертвование"""
    donation = DonationModel(**donation_data.dict())
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

@router.put("/{donation_id}", response_model=SDonationGet)
async def update_donation(
    db: DBDep,
    donation_id: int, 
    donation_data: SDonationUpdate, 
 
):
    """Обновить пожертвование"""
    donation = db.query(DonationModel).filter(DonationModel.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Пожертвование не найдено")
    
    for key, value in donation_data.dict(exclude_unset=True).items():
        setattr(donation, key, value)
    
    db.commit()
    db.refresh(donation)
    return donation

@router.delete("/{donation_id}")
async def delete_donation(db: DBDep,donation_id: int):
    """Удалить пожертвование"""
    donation = db.query(DonationModel).filter(DonationModel.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Пожертвование не найдено")
    
    db.delete(donation)
    db.commit()
    return {"message": "Пожертвование успешно удалено"}