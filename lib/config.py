import torch
import clip

MODEL_NAME = "ViT-B/32"
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load(MODEL_NAME, device=device)
