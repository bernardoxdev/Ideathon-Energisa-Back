from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from backend.core.database import Base

class TiposChamados(Base):
    __tablename__ = "tipos_chamados"

    id = Column(Integer, primary_key=True, autoincrement=True)

    tipo_chamado = Column(String(150), index=True, nullable=False)
    precisa_foto = Column(Boolean, default=False)

    chamados = relationship("Chamados", back_populates="tipo")