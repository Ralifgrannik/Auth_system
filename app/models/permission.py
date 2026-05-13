from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    resource = Column(String, nullable=False)   # projects, tasks, users и т.д.
    action = Column(String, nullable=False)     # read, create, update, delete...

    role = relationship("Role", back_populates="permissions")