from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.risk_core import process_risk_analysis
from backend.core.security import (
    require_role
)

from backend.models.risk_audit import RiskAudit
from backend.models.return_schemas import (
    RiskResponse
)

router = APIRouter(prefix="/risk", tags=["Risk"])

@router.post(
    "/classify", status_code=status.HTTP_200_OK,
    response_model=RiskResponse,
    summary="Classificar risco a partir de texto e imagem",
    description="Analisa um cenário usando texto e imagem e retorna o nível de risco",
    dependencies=[Depends(require_role("funcionarios", "admin", "owner"))]
)
async def classify_risk(
    texto: str = Form(..., min_length=3),
    imagem: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if imagem.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de imagem não suportado."
        )

    try:
        conteudo_imagem = await imagem.read()

        resultado, _ = process_risk_analysis(db, texto, conteudo_imagem)

        return RiskResponse(
            risco=resultado.risco,
            confianca=resultado.confianca,
            justificativa=resultado.justificativa
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@router.get(
    "/history", status_code=status.HTTP_200_OK,
    summary="Historico de classificaçoes",
    description="Pega todo o historico das classificacoes",
    dependencies = [Depends(require_role("funcionarios", "admin", "owner"))]
)
def listar_riscos(
    risco: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(RiskAudit)

    if risco:
        query = query.filter(RiskAudit.risco == risco)

    return query.order_by(RiskAudit.created_at.desc()).limit(100).all()