from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.core.database import get_db
from app.core.permissions import get_current_user
from app.models.user import User

router = APIRouter()

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    middle_name: Optional[str]
    is_active: bool
    roles: list[str]

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "middle_name": current_user.middle_name,
        "is_active": current_user.is_active,
        "roles": [role.name for role in current_user.roles]
    }


@router.patch("/me", response_model=UserResponse)
def update_user_info(
    update_data: UserUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновление данных пользователя"""
    if update_data.email and update_data.email != current_user.email:
        if db.query(User).filter(User.email == update_data.email).first():
            raise HTTPException(400, "Email already taken")

    if update_data.first_name is not None:
        current_user.first_name = update_data.first_name
    if update_data.last_name is not None:
        current_user.last_name = update_data.last_name
    if update_data.middle_name is not None:
        current_user.middle_name = update_data.middle_name
    if update_data.email is not None:
        current_user.email = update_data.email

    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Мягкое удаление аккаунта"""
    current_user.is_active = False
    db.commit()
    
    return {
        "message": "Account has been deactivated successfully",
        "note": "You have been logged out"
    }