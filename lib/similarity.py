# Similarity calculation utilities
from sklearn.metrics.pairwise import cosine_similarity
import torch

def calculate_cosine_similarity(embedding1, embedding2):
    if embedding1 is None or embedding2 is None:
        return None
    # Convert to numpy for sklearn
    emb1 = embedding1.cpu().numpy()
    emb2 = embedding2.cpu().numpy()
    return cosine_similarity(emb1, emb2)[0][0]

