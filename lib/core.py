import os
from tqdm import tqdm
from .embedding import load_image_embedding
from .similarity import calculate_cosine_similarity
from .ioUtils import list_image_files, write_output_mapping
from .config import model, preprocess

def match_images(reference_dir, query_dir, output_path):
    # Load reference embeddings
    reference_embeddings = {}
    reference_files = list_image_files(reference_dir)
    for path in reference_files:
        fname = os.path.basename(path)
        emb = load_image_embedding(path, model, preprocess)
        if emb is not None:
            reference_embeddings[fname] = emb

    # Query images
    mapping = []
    query_files = list_image_files(query_dir)
    for query_path in tqdm(query_files):
        query_name = os.path.basename(query_path)
        query_emb = load_image_embedding(query_path, model, preprocess)
        if query_emb is None:
            continue
        best_match = None
        best_score = -1
        for ref_name, ref_emb in reference_embeddings.items():
            score = calculate_cosine_similarity(query_emb, ref_emb)
            if score is not None and score > best_score:
                best_score = score
                best_match = ref_name
        mapping.append((query_name, best_match, best_score))

    # Save results
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    write_output_mapping(output_path, mapping)
    print(f"✅ Done! Saved mapping to {output_path}")
