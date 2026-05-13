from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.permissions import get_current_user
from app.models.role import Role

router = APIRouter(prefix="/roles", tags=["admin"])

@router.get("/")
def get_all_roles(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(403, "Only superuser allowed")
    return db.query(Role).all()