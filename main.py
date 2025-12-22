import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Импорт веб-роутера (для HTML страниц)
from app.api import web_router

# Импорт API роутеров для сущностей
from app.api.donations import router as donations_router
from app.api.project import router as projects_router  # обратите внимание на название файла project.py
from app.api.rewards import router as rewards_router
from app.api.roles import router as roles_router
from app.api.users import router as users_router

app = FastAPI(
    title="Crowdfunding Platform",
    version="1.0.0",
    description="Платформа для краудфандинговых проектов"
)

# Подключение статических файлов (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключение веб-роутера (HTML страницы) - должен быть ПЕРВЫМ
app.include_router(web_router)

# Подключение API роутеров
app.include_router(projects_router)
app.include_router(donations_router)
app.include_router(rewards_router)
app.include_router(users_router)
app.include_router(roles_router)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "ok", 
        "service": "Crowdfunding Platform API",
        "version": "1.0.0",
        "endpoints": {
            "projects": "/api/projects",
            "donations": "/api/donations", 
            "rewards": "/api/rewards",
            "users": "/api/users",
            "roles": "/api/roles",
            "web": "/"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
