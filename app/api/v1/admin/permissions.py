from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.permissions import get_current_user
from app.models.permission import Permission
from app.models.role import Role

router = APIRouter(prefix="/permissions", tags=["admin"])

class PermissionCreate(BaseModel):
    role_id: int
    resource: str
    action: str

@router.get("/")
def get_all_permissions(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(403, "Only superuser allowed")
    
    perms = db.query(Permission).all()
    return perms

@router.post("/")
def create_permission(data: PermissionCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(403, "Only superuser allowed")
    
    perm = Permission(
        role_id=data.role_id,
        resource=data.resource,
        action=data.action
    )
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm