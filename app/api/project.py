from fastapi import APIRouter, HTTPException
from typing import  Optional


from app.api.dependencies import DBDep
from app.schemes.projects import SProjectAdd, SProjectUpdate, SProjectGet
from app.services.projects import ProjectsService

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("/", response_model=list[SProjectGet])
async def get_projects(
    db: DBDep,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    category_id: Optional[int] = None,
    
):
    """Получить все проекты с фильтрацией"""
    
    projects = await ProjectsService(db).get_filtered_projects(offset=skip, limit=limit,user_id=user_id, category_id=category_id)
   
    return projects

@router.get("/{project_id}")
async def get_project(project_id: int, db: DBDep):
    """Получить проект по ID"""
    project = await ProjectsService(db).get_project(project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project

@router.post("/", response_model=SProjectGet, status_code=201)
async def create_project(project_data: SProjectAdd, db: DBDep):
    """Создать новый проект"""
    project = await ProjectsService(db).create_project(project_data)
    return project



@router.put("/{project_id}", response_model=None)
async def update_project(
    project_id: int,
    project_data: SProjectUpdate,
    db: DBDep
):
    """Обновить проект"""
    project = await db.projects.get_one_or_none(id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    await db.projects.edit(project_data, id=project_id)
    updated_project = await db.projects.get_one_or_none(id=project_id)
    return updated_project

@router.delete("/{project_id}")
async def delete_project(project_id: int, db: DBDep):
    """Удалить проект"""
    project = await db.projects.get_one_or_none(id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    await db.projects.delete(id=project_id)
    return {"message": "Проект успешно удален"}