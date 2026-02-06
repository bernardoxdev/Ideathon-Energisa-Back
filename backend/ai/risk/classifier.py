import joblib
from pathlib import Path
from backend.ai.risk.schema import RiskResult
from backend.ai.risk.vocab import ENERGISA_TERMS
from backend.ai.risk.utils import normalizar

MODEL_PATH = Path(__file__).parent / "model" / "risk_model.pkl"
_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def classificar_risco(descricao: str) -> RiskResult:
    model = get_model()

    texto = normalizar(descricao)

    probs = model.predict_proba([texto])[0]
    classes = model.classes_

    idx = int(probs.argmax())
    risco = str(classes[idx])
    confianca = float(probs[idx])

    termos_criticos = map(normalizar, ENERGISA_TERMS["critico"])
    if any(t in texto for t in termos_criticos):
        risco = "critico"
        confianca = max(confianca, 0.95)

    if risco == "medio" and confianca < 0.45:
        risco = "alto"

    return RiskResult(
        risco=risco,
        confianca=round(confianca, 2),
        justificativa=descricao
    )