from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Parceiros(Base):
    __tablename__ = "parceiros"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    telefone = Column(String(20), index=True, nullable=False)
    telefone_secundario = Column(String(20), index=True, nullable=True)

    email_secundario = Column(String(150), index=True, nullable=True)

    endereco = Column(String(300), index=True, nullable=True)

    prioridade = Column(Boolean, index=True, default=False)

    user = relationship("User", back_populates="parceiros")