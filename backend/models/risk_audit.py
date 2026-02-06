from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from backend.core.database import Base

class RiskAudit(Base):
    __tablename__ = "risk_audit"

    id = Column(Integer, primary_key=True)
    input_text = Column(Text, nullable=False)
    visual_description = Column(Text, nullable=False)

    risco = Column(String(20), nullable=False)
    confianca = Column(Float, nullable=False)

    model_version = Column(String(20), nullable=False)
    used_fallback = Column(String(10), nullable=False)
    explain_terms = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())