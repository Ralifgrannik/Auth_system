from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.models.permission import Permission

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Получение текущего пользователя по токену"""
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user = db.query(User).filter(
        User.id == int(payload["sub"]),
        User.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    return user


def has_permission(resource: str, action: str):
    """Основная зависимость для проверки прав доступа"""
    def dependency(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        
        has_right = db.query(Permission).filter(
            Permission.role_id.in_([role.id for role in current_user.roles]),
            Permission.resource == resource,
            Permission.action == action
        ).first()

        if not has_right:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: no permission for '{action}' on resource '{resource}'"
            )
        return current_user
    
    return dependency