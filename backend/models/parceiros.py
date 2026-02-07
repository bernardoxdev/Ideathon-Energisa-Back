from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Parceiros(Base):
    __tablename__ = "parceiros"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    telefone = Column(String(20), index=True, nullable=False)
    telefone_secundario = Column(String(20), index=True, nullable=True)

    email_secundario = Column(String(150), index=True, nullable=True)

    user = relationship("User", back_populates="parceiros")