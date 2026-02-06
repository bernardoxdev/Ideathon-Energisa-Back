from backend.ai.blip2.infer import analisar_cenario
from backend.ai.risk.classifier import classificar_risco

descricao = analisar_cenario(
    texto="Poste quebrado, motivo desconhecido",
    image_path="backend/tests/assets/poste.webp"
)
resultado = classificar_risco(descricao)

print({
    "descricao": descricao,
    "risco": resultado.risco,
    "confianca": resultado.confianca
})