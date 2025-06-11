import os
import torch
import clip
from PIL import Image
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity

device = "cuda" if torch.cuda.is_available() else "cpu"

REFERENCE_DIR = 'input/cartoon'
QUERY_DIR = 'output/extracted_images'
OUTPUT_PATH = 'output/output_mapping.csv'

def load_image_embedding(image_path, model, preprocess):
    try:
        image = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)
        with torch.no_grad():
            embedding = model.encode_image(image)
        return embedding / embedding.norm(dim=-1, keepdim=True)
    except Exception as e:
        print(f"❌ Failed to process {image_path}: {e}")
        return None

def main():
    model, preprocess = clip.load("ViT-B/32", device=device)

    # Load reference embeddings
    reference_embeddings = {}
    for fname in os.listdir(REFERENCE_DIR):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(REFERENCE_DIR, fname)
            emb = load_image_embedding(path, model, preprocess)
            if emb is not None:
                reference_embeddings[fname] = emb

    # Query images
    mapping = {}
    for query_name in tqdm(os.listdir(QUERY_DIR)):
        if not query_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        query_path = os.path.join(QUERY_DIR, query_name)
        query_emb = load_image_embedding(query_path, model, preprocess)
        if query_emb is None:
            continue

        best_match = None
        best_score = -1

        for ref_name, ref_emb in reference_embeddings.items():
            score = cosine_similarity(query_emb.cpu().numpy(), ref_emb.cpu().numpy())[0][0]
            if score > best_score:
                best_score = score
                best_match = ref_name

        mapping[query_name] = (best_match, best_score)

    # Save results
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        for k, (v, score) in mapping.items():
            f.write(f"{k} -> {v} (similarity: {score:.4f})\n")

    print(f"✅ Done! Saved mapping to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
