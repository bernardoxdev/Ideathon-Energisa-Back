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

    tokens = [
        t for t in texto.split()
        if t not in STOPWORDS_TECNICAS
    ]

    return " ".join(tokens)

def expandir_frase(frase: str):
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

def limpar_contextos_duplicados(texto: str) -> str:
    linhas = re.split(r'\.\s*', texto)

    vistos = set()
    resultado = []

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        if ":" in linha:
            rotulo, conteudo = linha.split(":", 1)
            chave = normalizar(conteudo)
        else:
            rotulo = None
            conteudo = linha
            chave = normalizar(linha)

        if not chave or chave in vistos:
            continue

        vistos.add(chave)

        if rotulo:
            resultado.append(f"{rotulo.strip()}: {conteudo.strip()}")
        else:
            resultado.append(conteudo.strip())

    return ". ".join(resultado) + "."