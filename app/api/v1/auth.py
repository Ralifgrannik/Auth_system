from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.permissions import get_current_user
from app.models.user import User

router = APIRouter()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None


# ====================== REGISTER ======================
@router.post("/register", response_model=TokenResponse)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)

    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        middle_name=user_data.middle_name,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Создаём токен
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token}


# ====================== LOGIN ======================
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """Логин (работает и через Swagger Authorize)"""
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=401, 
            detail="Account is deactivated"
        )

    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


# ====================== LOGOUT ======================
@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Выход из системы"""
    return {
        "message": "Successfully logged out",
        "note": "Delete the token on the client side"
    }


# ====================== ПРОВЕРКА ТОКЕНА ======================
@router.get("/me", response_model=dict)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Получить информацию о текущем пользователе по токену"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "middle_name": current_user.middle_name,
        "is_active": current_user.is_active,
        "roles": [role.name for role in current_user.roles]
    }