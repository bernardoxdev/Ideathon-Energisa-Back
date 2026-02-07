import os
import tempfile
from contextlib import contextmanager
from sqlalchemy.orm import Session

from backend.ai.blip2.infer import analisar_cenario
from backend.ai.risk.classifier import classificar_risco, get_model
from backend.ai.risk.explain import explain_decision
from backend.ai.risk.utils import normalizar
from backend.models.risk_audit import RiskAudit

@contextmanager
def handle_temp_image(image_bytes: bytes):
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name
        yield tmp_path
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

def process_risk_analysis(db: Session, texto_usuario: str, imagem_bytes: bytes):
    with handle_temp_image(imagem_bytes) as tmp_path:
        descricao_visual = analisar_cenario(texto_usuario, tmp_path)

        descricao_completa = (
            f"Descrição visual: {descricao_visual}. "
            f"Contexto adicional informado: {texto_usuario}"
        )

        resultado = classificar_risco(descricao_completa)

        modelo = get_model()
        termos_explicativos = explain_decision(
            modelo,
            normalizar(descricao_completa),
            top_k=5
        )

        audit = RiskAudit(
            input_text=texto_usuario,
            visual_description=descricao_visual,
            risco=resultado.risco,
            confianca=resultado.confianca,
            model_version="v1",
            used_fallback=str(resultado.fallback_usado),
            explain_terms=", ".join(termos_explicativos)
        )

        db.add(audit)
        db.commit()
        db.refresh(audit)

        return resultado, audit