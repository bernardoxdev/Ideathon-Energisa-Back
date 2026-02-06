import re
import unidecode

STOPWORDS_TECNICAS = {
    "ocorrencia", "registrada", "situacao", "observada",
    "risco", "identificado", "apos", "proximo"
}

def normalizar(texto: str) -> str:
    texto = texto.lower()
    texto = unidecode.unidecode(texto)
    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    # remove stopwords técnicas pouco informativas
    tokens = [
        t for t in texto.split()
        if t not in STOPWORDS_TECNICAS
    ]

    return " ".join(tokens)

def expandir_frase(frase: str):
    """
    Expansão orientada a relatórios reais de campo
    """
    return [
        frase,
        f"{frase} em area urbana",
        f"{frase} em via publica",
        f"{frase} proximo a residencias",
        f"{frase} apos chuva forte",
        f"{frase} apos colisao veicular",
        f"{frase} com risco a populacao",
        f"{frase} exigindo intervencao imediata",
        f"ocorrencia tecnica: {frase}",
        f"registro de campo: {frase}",
    ]