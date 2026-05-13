# Тестовое задание
Реализация системы аутентификации и авторизации на FastAPI.

## Основные возможности

- Регистрация и авторизация пользователей
- Система прав доступа 
- Role-Based + Permission-Based доступ
- Мягкое удаление пользователей
- Админ-панель для управления ролями и правами

## Схема базы данных

### Основные таблицы:

- **users** — пользователи (`is_active`, `is_superuser`)
- **roles** — роли (`admin`, `manager`, `viewer`)
- **user_roles** — связь многие-ко-многим
- **permissions** — granular права (`resource` + `action`)

**Принцип работы прав:**
Пользователь → Роли → Permissions (`resource`, `action`)

Пример: `projects` + `create`, `tasks` + `read` и т.д.

## Как запустить

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python seed.py
python run.py

# link: http://127.0.0.1:8000/docs
