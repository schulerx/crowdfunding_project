from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate, DonationResponse

router = APIRouter(prefix="/api/donations", tags=["donations"])

@router.get("/", response_model=List[DonationResponse])
async def get_donations(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = None,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Получить все пожертвования с фильтрацией"""
    query = db.query(Donation)
    
    if user_id:
        query = query.filter(Donation.user_id == user_id)
    if project_id:
        query = query.filter(Donation.project_id == project_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{donation_id}", response_model=DonationResponse)
async def get_donation(donation_id: int, db: Session = Depends(get_db)):
    """Получить пожертвование по ID"""
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Пожертвование не найдено")
    return donation

@router.post("/", response_model=DonationResponse, status_code=201)
async def create_donation(donation_data: DonationCreate, db: Session = Depends(get_db)):
    """Создать новое пожертвование"""
    donation = Donation(**donation_data.dict())
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

@router.put("/{donation_id}", response_model=DonationResponse)
async def update_donation(
    donation_id: int, 
    donation_data: DonationUpdate, 
    db: Session = Depends(get_db)
):
    """Обновить пожертвование"""
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Пожертвование не найдено")
    
    for key, value in donation_data.dict(exclude_unset=True).items():
        setattr(donation, key, value)
    
    db.commit()
    db.refresh(donation)
    return donation

@router.delete("/{donation_id}")
async def delete_donation(donation_id: int, db: Session = Depends(get_db)):
    """Удалить пожертвование"""
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Пожертвование не найдено")
    
    db.delete(donation)
    db.commit()
    return {"message": "Пожертвование успешно удалено"}