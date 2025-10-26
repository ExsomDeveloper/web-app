from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import CORS_ORIGINS, HOST, PORT
from routers import products, tryon

app = FastAPI(title="Telegram Try-On API", version="1.0.0")

# Настройка CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(products.router)
app.include_router(tryon.router)


@app.get("/")
async def root():
    return {"message": "Telegram Try-On API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, reload=True)
