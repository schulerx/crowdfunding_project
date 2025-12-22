from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.api.dependencies import DBDep
from app.models.categories import CategoriesModel
from app.schemes.categories import SCategoriesAdd, SCategoriesUpdate, SCategoriesGet

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("/", response_model=List[SCategoriesGet])
async def get_categories(skip: int = 0, limit: int = 100, db = DBDep):
    """Получить все категории"""
    return db.query(CategoriesModel).offset(skip).limit(limit).all()

@router.get("/{category_id}", response_model=SCategoriesGet)
async def get_category(category_id: int, db = DBDep):
    """Получить категорию по ID"""
    category = db.query(CategoriesModel).filter(CategoriesModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category

@router.post("/", response_model=SCategoriesGet, status_code=201)
async def create_category(category_data: SCategoriesAdd, db = DBDep):
    """Создать новую категорию"""
    category = CategoriesModel(**category_data.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.put("/{category_id}", response_model=SCategoriesGet)
async def update_category(
    category_id: int, 
    category_data: SCategoriesUpdate, 
    db = DBDep
):
    """Обновить категорию"""
    category = db.query(CategoriesModel).filter(CategoriesModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    for key, value in category_data.dict(exclude_unset=True).items():
        setattr(category, key, value)
    
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}")
async def delete_category(category_id: int, db = DBDep):
    """Удалить категорию"""
    category = db.query(CategoriesModel).filter(CategoriesModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    db.delete(category)
    db.commit()
    return {"message": "Категория успешно удалена"}