from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import web

app = FastAPI(title="Краудфандинговая платформа")

# Подключение статических файлов (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключение веб-роутера
app.include_router(web.router)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Сервер работает"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
