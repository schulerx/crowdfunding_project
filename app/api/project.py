from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.api.dependencies import DBDep
from app.models.project import ProjectModel
from app.schemes.projects import SProjectAdd, SProjectUpdate, SProjectGet

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("/", response_model=List[SProjectGet])
async def get_projects(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db = DBDep
):
    """Получить все проекты с фильтрацией"""
    query = db.session.query(ProjectModel)
    
    if user_id:
        query = query.filter(ProjectModel.user_id == user_id)
    if category_id:
        query = query.filter(ProjectModel.category_id == category_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{project_id}", response_model=SProjectGet)
async def get_project(project_id: int, db = DBDep):
    """Получить проект по ID"""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project

@router.post("/", response_model=SProjectGet, status_code=201)
async def create_project(project_data: SProjectAdd, db = DBDep):
    """Создать новый проект"""
    project = ProjectModel(**project_data.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.put("/{project_id}", response_model=SProjectGet)
async def update_project(
    project_id: int, 
    project_data: SProjectUpdate, 
    db = DBDep
):
    """Обновить проект"""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    for key, value in project_data.dict(exclude_unset=True).items():
        setattr(project, key, value)
    
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
async def delete_project(project_id: int, db = DBDep):
    """Удалить проект"""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    db.delete(project)
    db.commit()
    return {"message": "Проект успешно удален"}