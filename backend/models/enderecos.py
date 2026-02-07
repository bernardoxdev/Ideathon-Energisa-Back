from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Enderecos(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cep = Column(String(10), index=True, nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(20), nullable=False)
    cidade = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)

    chamados = relationship("Chamados", back_populates="endereco")