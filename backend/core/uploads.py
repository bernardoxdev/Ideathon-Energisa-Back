import os
import uuid
from fastapi import UploadFile

BASE_DIR = "uploads"
os.makedirs(BASE_DIR, exist_ok=True)

def salvar_imagem(file: UploadFile, pasta: str) -> str:
    ext = file.filename.split(".")[-1]
    nome = f"{uuid.uuid4()}.{ext}"

    caminho = os.path.join(BASE_DIR, pasta)
    os.makedirs(caminho, exist_ok=True)

    full_path = os.path.join(caminho, nome)

    with open(full_path, "wb") as f:
        f.write(file.file.read())

    return full_path
