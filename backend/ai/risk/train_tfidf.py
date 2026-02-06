import joblib
from sklearn.calibration import CalibratedClassifierCV

from backend.ai.risk.vocab import ENERGISA_TERMS
from backend.ai.risk.utils import normalizar, expandir_frase
from backend.ai.risk.model_factory import create_pipeline

X = []
y = []

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

joblib.dump(model, "backend/ai/risk/model/risk_model.pkl")

print("✅ Modelo TF-IDF aprimorado treinado com sucesso")