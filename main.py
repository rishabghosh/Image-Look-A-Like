import os
from PIL import Image
import imagehash
from tqdm import tqdm

# Config
REFERENCE_IMAGES_DIR = "input/cartoon"
QUERY_IMAGES_DIR = "output/extracted_images"
OUTPUT_CSV = "output/output_mapping.csv"
THRESHOLD = 10  # Adjust based on accuracy needs

def compute_hash(image_path):
    try:
        image = Image.open(image_path)
        return imagehash.average_hash(image)
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

def main():
    # Load all reference images
    reference_hashes = {}
    for fname in os.listdir(REFERENCE_IMAGES_DIR):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(REFERENCE_IMAGES_DIR, fname)
            h = compute_hash(path)
            if h:
                reference_hashes[fname] = h

    print(f"✅ Loaded {len(reference_hashes)} reference images from {REFERENCE_IMAGES_DIR}")

    # Load query images
    query_images = [f for f in os.listdir(QUERY_IMAGES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"🔍 Comparing {len(query_images)} extracted images from {QUERY_IMAGES_DIR}")

    # Compare
    mapping = {}

    for query in tqdm(query_images):
        query_path = os.path.join(QUERY_IMAGES_DIR, query)
        query_hash = compute_hash(query_path)
        if not query_hash:
            continue

        best_match = None
        min_distance = float('inf')

        for ref_name, ref_hash in reference_hashes.items():
            distance = query_hash - ref_hash
            if distance < min_distance:
                min_distance = distance
                best_match = ref_name

        if best_match and min_distance < THRESHOLD:
            mapping[query] = best_match
        else:
            print(f"🚫 No close match found for {query} (min distance: {min_distance})")

    # Write to CSV
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, 'w') as f:
        for q, r in mapping.items():
            f.write(f"{q} -> {r}\n")

    print(f"\n✅ Matching complete. Results saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
