from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    user = relationship("User", back_populates="admin")