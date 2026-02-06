from dataclasses import dataclass
from typing import Literal

RiskLevel = Literal["baixo", "medio", "alto", "critico"]


@dataclass
class RiskResult:
    risco: RiskLevel
    confianca: float
    justificativa: str
    fallback_usado: bool
