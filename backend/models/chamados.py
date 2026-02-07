from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base

class Chamados(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, autoincrement=True)

    protocolo = Column(String(50), unique=True, index=True, nullable=False)
    descricao = Column(String(1000), nullable=False)
    status = Column(String(50), index=True, nullable=False)

    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    endereco_id = Column(Integer, ForeignKey("enderecos.id"), nullable=False)
    tipo_id = Column(Integer, ForeignKey("tipos_chamados.id"), nullable=False)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tipo = relationship("TiposChamados", back_populates="chamados")
    endereco = relationship("Enderecos", back_populates="chamados")
    cliente = relationship("User")