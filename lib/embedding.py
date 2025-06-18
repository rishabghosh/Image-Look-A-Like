# Image embedding utilities
import torch
from PIL import Image
from .config import device

def load_image_embedding(image_path, model, preprocess):
    try:
        image = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)
        with torch.no_grad():
            embedding = model.encode_image(image)
        return embedding / embedding.norm(dim=-1, keepdim=True)
    except Exception as e:
        print(f"❌ Failed to process {image_path}: {e}")
        return None

