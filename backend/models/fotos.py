from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.core.database import Base

class Fotos(Base):
    __tablename__ = "fotos"

    id = Column(Integer, primary_key=True, autoincrement=True)

    caminho = Column(String(500), nullable=False)
    origem = Column(String(20), nullable=False)

    chamado_id = Column(Integer, ForeignKey("chamados.id", ondelete="CASCADE"), nullable=True)
    solicitacao_id = Column(Integer, ForeignKey("solicitacoes.id", ondelete="CASCADE"), nullable=True)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())