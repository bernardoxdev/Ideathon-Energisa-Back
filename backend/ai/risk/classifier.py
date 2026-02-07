import joblib
from pathlib import Path
from deep_translator import GoogleTranslator

from backend.ai.risk.train_runner import train_if_needed
from backend.ai.risk.schema import RiskResult
from backend.ai.risk.vocab import ENERGISA_TERMS
from backend.ai.risk.utils import normalizar, limpar_contextos_duplicados

MODEL_PATH = Path(__file__).parent / "model" / "risk_model.pkl"
_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def classificar_risco(descricao: str) -> RiskResult:
    train_if_needed()

    model = get_model()

    texto_normalizado = normalizar(descricao)

    probs = model.predict_proba([texto_normalizado])[0]
    classes = model.classes_

    idx = int(probs.argmax())
    risco = str(classes[idx])
    confianca = float(probs[idx])

    fallback_usado = False

    termos_criticos = map(normalizar, ENERGISA_TERMS["critico"])
    if any(t in texto_normalizado for t in termos_criticos):
        risco = "critico"
        confianca = max(confianca, 0.95)
        fallback_usado = True

    if risco == "medio" and confianca < 0.45:
        risco = "alto"
        fallback_usado = True

    descricao_traduzida = GoogleTranslator(
        source="auto",
        target="pt"
    ).translate(descricao)

    analise_modelo = (
        "presença de poste tombado em via pública, "
        "indicando risco potencial à segurança e à circulação"
        if risco in ["alto", "critico"]
        else "situação identificada sem indícios imediatos de risco crítico"
    )

    descricao_limpa = limpar_contextos_duplicados(descricao_traduzida)

    justificativa = (
        f"ANÁLISE DO MODELO: {analise_modelo} / "
        f"DESCRIÇÃO INFORMADA: {descricao_limpa}"
    )

    return RiskResult(
        risco=risco,
        confianca=round(confianca, 2),
        justificativa=justificativa,
        fallback_usado=fallback_usado
    )