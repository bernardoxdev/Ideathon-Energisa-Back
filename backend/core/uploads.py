import os
import uuid
from fastapi import UploadFile, HTTPException

BASE_UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_IMAGE_TYPES = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/webp": "webp",
}

def salvar_imagem(arquivo: UploadFile, pasta: str) -> str:
    if arquivo.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(400, "Tipo de imagem não permitido")

    upload_dir = os.path.join(BASE_UPLOAD_DIR, pasta)
    os.makedirs(upload_dir, exist_ok=True)

    ext = ALLOWED_IMAGE_TYPES[arquivo.content_type]
    nome_arquivo = f"{uuid.uuid4()}.{ext}"
    caminho = os.path.join(upload_dir, nome_arquivo)

    tamanho = 0

    try:
        with open(caminho, "wb") as f:
            while chunk := arquivo.file.read(1024 * 1024):
                tamanho += len(chunk)
                if tamanho > MAX_FILE_SIZE:
                    raise HTTPException(413, "Imagem muito grande")
                f.write(chunk)

        return caminho

    except Exception:
        if os.path.exists(caminho):
            os.remove(caminho)
        raise