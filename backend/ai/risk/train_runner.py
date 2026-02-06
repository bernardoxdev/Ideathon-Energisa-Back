from pathlib import Path
import joblib

from backend.ai.risk.vocab import ENERGISA_TERMS
from backend.ai.risk.utils import normalizar, expandir_frase
from backend.ai.risk.model_factory import create_pipeline
from sklearn.calibration import CalibratedClassifierCV

MODEL_DIR = Path(__file__).parent / "model"
MODEL_PATH = MODEL_DIR / "risk_model.pkl"

def train_if_needed(force: bool = False):
    if MODEL_PATH.exists() and not force:
        print("[RISK] Modelo já existe. Treino ignorado.")
        return

    print("[RISK] Treinando modelo TF-IDF...")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    X, y = [], []

    for label, frases in ENERGISA_TERMS.items():
        for frase in frases:
            for variante in expandir_frase(frase):
                X.append(normalizar(variante))
                y.append(label)

    pipeline = create_pipeline()

    model = CalibratedClassifierCV(
        pipeline,
        method="sigmoid",
        cv=3
    )

    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    print("[RISK] Modelo treinado e salvo com sucesso.")
