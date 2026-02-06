from backend.ai.blip2.infer import analisar_cenario

descricao = analisar_cenario(
    texto="Broken pole near school",
    image_path="backend/tests/assets/poste.webp"
)

print("DESCRIÇÃO:", descricao)