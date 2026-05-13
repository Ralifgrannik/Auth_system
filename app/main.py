from fastapi import FastAPI
from app.core.database import engine, Base
import app.models  # Регистрация всех моделей

from app.api.v1 import auth, users, mock_resources
from app.api.v1.admin import roles, permissions   # Админские роуты

app = FastAPI(
    title="Custom Authentication & Authorization System",
    description="Собственная система аутентификации и авторизации (без готовых решений фреймворка)",
    version="1.0.0"
)

# Подключение роутеров
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(mock_resources.router, prefix="/api/v1", tags=["Business Resources"])
app.include_router(roles.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(permissions.router, prefix="/api/v1/admin", tags=["Admin"])

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created / already exist")

@app.get("/")
def root():
    return {
        "message": "✅ Custom Auth System is running",
        "docs": "/docs",
        "test_users": {
            "admin": "admin@example.com / admin123",
            "manager": "manager@example.com / manager123"
        }
    }