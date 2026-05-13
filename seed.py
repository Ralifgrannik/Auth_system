from app.core.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.core.security import get_password_hash

def seed_data():
    db = SessionLocal()

    # Создаём роли
    roles = {
        "admin": "Administrator - full access",
        "manager": "Manager - can manage projects and tasks",
        "viewer": "Viewer - read only"
    }

    role_objects = {}
    for name, desc in roles.items():
        role = db.query(Role).filter(Role.name == name).first()
        if not role:
            role = Role(name=name, description=desc)
            db.add(role)
            db.commit()
            db.refresh(role)
        role_objects[name] = role

    # Создаём права доступа (Permissions)
    permissions = [
        # Admin - всё
        ("admin", "projects", "read"),
        ("admin", "projects", "create"),
        ("admin", "projects", "update"),
        ("admin", "projects", "delete"),
        ("admin", "tasks", "read"),
        ("admin", "tasks", "create"),
        ("admin", "tasks", "update"),
        ("admin", "users", "read"),

        # Manager
        ("manager", "projects", "read"),
        ("manager", "projects", "create"),
        ("manager", "projects", "update"),
        ("manager", "tasks", "read"),
        ("manager", "tasks", "create"),
        ("manager", "tasks", "update"),

        # Viewer
        ("viewer", "projects", "read"),
        ("viewer", "tasks", "read"),
    ]

    for role_name, resource, action in permissions:
        role = role_objects[role_name]
        exists = db.query(Permission).filter(
            Permission.role_id == role.id,
            Permission.resource == resource,
            Permission.action == action
        ).first()
        
        if not exists:
            perm = Permission(role_id=role.id, resource=resource, action=action)
            db.add(perm)

    # Создаём тестового администратора
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin_user:
        admin = User(
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            first_name="Super",
            last_name="Admin",
            is_active=True,
            is_superuser=True
        )
        admin.roles.append(role_objects["admin"])
        db.add(admin)

    # Создаём обычного пользователя (менеджер)
    manager_user = db.query(User).filter(User.email == "manager@example.com").first()
    if not manager_user:
        manager = User(
            email="manager@example.com",
            password_hash=get_password_hash("manager123"),
            first_name="Ivan",
            last_name="Ivanov",
            is_active=True
        )
        manager.roles.append(role_objects["manager"])
        db.add(manager)

    db.commit()
    print("✅ Seed data успешно загружен!")
    db.close()

if __name__ == "__main__":
    seed_data()