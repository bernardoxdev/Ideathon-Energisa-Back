from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Funcionarios(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    documento = Column(String(30), index=True, nullable=True)
    role = Column(String(30), index=True, nullable=True) # Tecnico, Suporte

    user = relationship("User", back_populates="funcionarios")