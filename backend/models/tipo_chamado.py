from sqlalchemy import Column, Integer, String, Boolean
from backend.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    tipo_chamado = Column(String(150), index=True, nullable=False)
    precisa_foto = Column(Boolean, index=True, default=False)