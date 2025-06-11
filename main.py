
import os
import pandas as pd
from PIL import Image
import imagehash
from tqdm import tqdm
from collections import defaultdict

# Config
EXCEL_PATH = "input/cartoon.xlsx"
IMAGES_FOLDER = "input/cartoon"
OUTPUT_CSV = "output/output_mapping.csv"

def compute_hash(image_path):
    try:
        image = Image.open(image_path)
        return imagehash.average_hash(image)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def main():
    # Load product data
    df = pd.read_excel(EXCEL_PATH)
    products = []

    for _, row in df.iterrows():
        pid = row['Product ID']
        products.append((pid, row.get('Front Image'), row.get('Back Image'), row.get('Front side')))

    # Compute hashes for reference images if available
    reference_hashes = defaultdict(list)

    for pid, front, back, side in products:
        for label, col in zip(['f', 'b', 's'], [front, back, side]):
            if pd.notna(col):
                ref_path = os.path.join(IMAGES_FOLDER, col)
                h = compute_hash(ref_path)
                if h:
                    reference_hashes[pid].append((h, label))

    # Now match all images in the folder
    mapping = defaultdict(list)
    all_images = [f for f in os.listdir(IMAGES_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for img in tqdm(all_images):
        img_path = os.path.join(IMAGES_FOLDER, img)
        h = compute_hash(img_path)
        if h is None:
            continue

        best_match = None
        best_dist = 100  # Arbitrary large number
        matched_labels = []

        for pid, refs in reference_hashes.items():
            for ref_hash, label in refs:
                dist = h - ref_hash
                if dist < 10:  # Threshold for matching
                    matched_labels.append(f"{pid}-{label}")

        if len(set(i.split('-')[0] for i in matched_labels)) == 1 and len(matched_labels) == 1:
            # Only one type of image for that product
            mapping[img].append(matched_labels[0].split('-')[0])
        else:
            mapping[img].extend(matched_labels)

    # Write output CSV
    with open(OUTPUT_CSV, 'w') as f:
        for k, v in mapping.items():
            f.write(f"{k} -> {v}\n")

if __name__ == "__main__":
    main()
