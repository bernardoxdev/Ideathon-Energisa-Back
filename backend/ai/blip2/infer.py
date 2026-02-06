from PIL import Image
import torch
from .loader import model, processor, HAS_GPU
from .prompt import RISK_PROMPT

def analisar_cenario(texto: str, image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")

    prompt = f"""
{RISK_PROMPT}

TEXTO DO USUÁRIO:
{texto}

DESCRIÇÃO:
"""

    if HAS_GPU:
        inputs = processor(
            images=image,
            text=prompt,
            return_tensors="pt"
        ).to(model.device)

        with torch.inference_mode():
            output = model.generate(
                **inputs,
                max_new_tokens=80
            )

        return processor.decode(output[0], skip_special_tokens=True)

    else:
        inputs = processor(
            images=image,
            return_tensors="pt"
        )

        with torch.inference_mode():
            output = model.generate(
                **inputs,
                max_new_tokens=60
            )

        legenda = processor.decode(output[0], skip_special_tokens=True)

        return f"{legenda}. Contexto adicional: {texto}"