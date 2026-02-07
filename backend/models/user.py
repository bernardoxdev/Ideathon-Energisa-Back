from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    parceiros = relationship("Parceiros", back_populates="user", uselist=False, cascade="all, delete")
    funcionarios = relationship("Funcionarios", back_populates="user", uselist=False, cascade="all, delete")
    admin = relationship("Admin", back_populates="user", uselist=False, cascade="all, delete")
    # usuarios
    # parceiros (Pode ver chamados abertos, marcar status de parceiro no chamado)
    # funcionarios (Pode ver chamados abertos, solicitaçoes de chamados, fechar chamados, ver dados de usuarios e parceiros)
    # admin (Permissao all)
    # owner (Permissao de

    # Endereço e Demanda
    # Carga Alta nao precisa de foto
    # Fotos: Arvore caida, poste caido, acidente (opcional), Inspençao de rede
    # Toque acidental, Construçao Civil, Telecom, Furto