from fastapi import APIRouter, Depends
from app.core.permissions import has_permission

router = APIRouter()

# === Mock ресурсы для демонстрации системы прав ===

@router.get("/projects")
def get_projects(current_user = Depends(has_permission("projects", "read"))):
    return {
        "projects": [
            {"id": 1, "name": "Project Alpha", "status": "active"},
            {"id": 2, "name": "Project Beta", "status": "pending"}
        ],
        "user": f"{current_user.first_name} {current_user.last_name}"
    }


@router.post("/projects")
def create_project(current_user = Depends(has_permission("projects", "create"))):
    return {"message": "Project created successfully", "user": current_user.email}


@router.get("/tasks")
def get_tasks(current_user = Depends(has_permission("tasks", "read"))):
    return {
        "tasks": ["Task 1 - Design", "Task 2 - Development"],
        "user": current_user.email
    }


@router.get("/admin-only")
def admin_only(current_user = Depends(has_permission("users", "read"))):
    """Пример ресурса, доступного только администратору"""
    return {"message": "This is admin only content", "user": current_user.email}