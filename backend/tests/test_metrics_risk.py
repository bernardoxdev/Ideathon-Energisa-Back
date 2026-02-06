from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from backend.ai.risk.classifier import classificar_risco

TEST_DATA = [
    ("Explosão em subestação urbana próxima a hospital", "critico"),
    ("Incêndio com arco elétrico em área pública", "critico"),
    ("Condutor energizado caído após colisão com veículo", "alto"),
    ("Poste inclinado sobre calçada em via movimentada", "alto"),
    ("Vegetação encostando na rede elétrica em área rural", "medio"),
    ("Transformador com sinais de desgaste", "medio"),
    ("Inspeção visual sem anormalidades identificadas", "baixo"),
    ("Rede elétrica em funcionamento regular", "baixo"),
]

def test_metricas_risco():
    y_true = []
    y_pred = []

    for texto, risco_esperado in TEST_DATA:
        resultado = classificar_risco(texto)
        y_true.append(risco_esperado)
        y_pred.append(resultado.risco)

    acc = accuracy_score(y_true, y_pred)

    print("\nAccuracy:", acc)
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, zero_division=0))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))

    assert acc >= 0.4

def test_nunca_classificar_critico_como_baixo():
    textos_criticos = [
        "Incêndio em poste próximo a escola",
        "Explosão com arco elétrico em área urbana",
        "Condutor energizado no solo com pedestres próximos",
        "Choque elétrico em via pública"
    ]

    for texto in textos_criticos:
        resultado = classificar_risco(texto)
        assert resultado.risco in ["critico", "alto"]

def test_confianca_critico_alta():
    textos = [
        "Incêndio em subestação urbana",
        "Explosão com risco de choque elétrico"
    ]

    for texto in textos:
        resultado = classificar_risco(texto)
        assert resultado.confianca >= 0.8