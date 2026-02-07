import torch

HAS_GPU = torch.cuda.is_available()

_model = None
_processor = None
_model_name = None

def load_blip2():
    global _model, _processor, _model_name

    if _model is not None and _processor is not None:
        return _model, _processor, HAS_GPU

    if HAS_GPU:
        from transformers import Blip2Processor, Blip2ForConditionalGeneration

        _model_name = "Salesforce/blip2-flan-t5-xl"

        print("🚀 Carregando BLIP-2 (GPU)...")

        _processor = Blip2Processor.from_pretrained(_model_name)

        _model = Blip2ForConditionalGeneration.from_pretrained(
            _model_name,
            device_map="auto",
            torch_dtype=torch.float16
        ).eval()

    else:
        from transformers import BlipProcessor, BlipForConditionalGeneration

        _model_name = "Salesforce/blip-image-captioning-large"

        print("🐌 Carregando BLIP (CPU)...")

        _processor = BlipProcessor.from_pretrained(
            _model_name,
            use_fast=False
        )

        _model = BlipForConditionalGeneration.from_pretrained(
            _model_name
        ).eval()

    print(f"✅ Modelo carregado: {_model_name}")
    return _model, _processor, HAS_GPU