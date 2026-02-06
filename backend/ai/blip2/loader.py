import torch

HAS_GPU = torch.cuda.is_available()

if HAS_GPU:
    from transformers import Blip2Processor, Blip2ForConditionalGeneration

    MODEL_NAME = "Salesforce/blip2-flan-t5-xl"

    processor = Blip2Processor.from_pretrained(MODEL_NAME)

    model = Blip2ForConditionalGeneration.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        torch_dtype=torch.float16
    ).eval()
else:
    from transformers import BlipProcessor, BlipForConditionalGeneration

    MODEL_NAME = "Salesforce/blip-image-captioning-large"

    processor = BlipProcessor.from_pretrained(
        MODEL_NAME,
        use_fast=False
    )

    model = BlipForConditionalGeneration.from_pretrained(
        MODEL_NAME
    ).eval()