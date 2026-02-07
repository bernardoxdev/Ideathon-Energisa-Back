from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    telefone = Column(Integer, index=True, nullable=False)

    user = relationship("User", back_populates="usuario")