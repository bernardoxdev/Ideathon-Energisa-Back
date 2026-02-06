from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel
import tempfile
import os

from backend.ai.blip2.infer import analisar_cenario
from backend.ai.risk.classifier import classificar_risco
from backend.ai.risk.schema import RiskResult

router = APIRouter(prefix="/risk", tags=["Risk"])

class RiskResponse(BaseModel):
    risco: str
    confianca: float
    justificativa: str

@router.post(
    "/classify",
    status_code=status.HTTP_200_OK,
    response_model=RiskResponse,
    summary="Classificar risco a partir de texto e imagem",
    description="Analisa um cenário usando texto e imagem e retorna o nível de risco"
)
async def classify_risk(
    texto: str = Form(..., min_length=3),
    imagem: UploadFile = File(...)
):
    if imagem.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de imagem não suportado. Use JPG ou PNG."
        )

    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(await imagem.read())
            tmp_path = tmp.name

        descricao_visual = analisar_cenario(texto, tmp_path)

        descricao_completa = (
            f"Descrição visual: {descricao_visual}. "
            f"Contexto adicional informado: {texto}"
        )

        resultado: RiskResult = classificar_risco(descricao_completa)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar classificação de risco: {str(e)}"
        )

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    return RiskResponse(
        risco=resultado.risco,
        confianca=resultado.confianca,
        justificativa=resultado.justificativa
    )