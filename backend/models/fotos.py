from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base

class Fotos(Base):
    __tablename__ = "fotos"

    id = Column(Integer, primary_key=True, autoincrement=True)

    nome_original = Column(String, nullable=False)
    nome_armazenado = Column(String, nullable=False)
    caminho = Column(String, nullable=False)
    origem = Column(String(20), nullable=False)

    content_type = Column(String, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    chamado_id = Column(Integer, ForeignKey("chamados.id", ondelete="CASCADE"), nullable=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacoes.id", ondelete="CASCADE"), nullable=True)

    chamado = relationship("Chamados", back_populates="fotos")
    solicitacao = relationship("Solicitacoes", back_populates="fotos")