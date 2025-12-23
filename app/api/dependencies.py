from typing import Annotated

from fastapi import Depends, Request, HTTPException, status
from pydantic import BaseModel, Field

from app.database.database import async_session_maker
from app.exceptions.auth import (
    InvalidJWTTokenError,
    InvalidTokenHTTPError,
    NoAccessTokenHTTPError,
    IsNotAdminHTTPError,
)
from app.services.auth import AuthService
from app.database.db_manager import DBManager, get_db_manager


class PaginationParams(BaseModel):
    page: int | None = Field(default=1, ge=1)
    per_page: int | None = Field(default=10, ge=1, le=100)
    sort_by: str | None = Field(default="created_at")
    sort_order: str | None = Field(default="desc", regex="^(asc|desc)$")


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    """Получение токена из cookies или заголовков"""
    token = request.cookies.get("access_token")
    if token:
        return token
    
    # Проверяем Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.replace("Bearer ", "")
    
    raise NoAccessTokenHTTPError


def get_current_user_id(token: str = Depends(get_token)) -> int:
    """Получение ID текущего пользователя из токена"""
    try:
        data = AuthService.decode_token(token)
        return data["user_id"]
    except InvalidJWTTokenError:
        raise InvalidTokenHTTPError
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db() -> AsyncGenerator[DBManager, None]:
    """Зависимость для получения DBManager"""
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


async def check_is_admin(db: DBDep, user_id: UserIdDep) -> bool:
    """Проверка, является ли пользователь администратором"""
    try:
        user = await db.users.get_one_or_none_with_role(id=user_id)
        
        if not user or not user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User or role not found"
            )
        
        if user.role.name.lower() == "admin":
            return True
            
        raise IsNotAdminHTTPError
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking admin status: {str(e)}"
        )


IsAdminDep = Annotated[bool, Depends(check_is_admin)]


async def get_current_user(db: DBDep, user_id: UserIdDep):
    """Получение объекта текущего пользователя"""
    user = await db.users.get_one_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]