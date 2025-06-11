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
THRESHOLD = 20  # Adjust this if needed

def compute_hash(image_path):
    try:
        image = Image.open(image_path)
        return imagehash.average_hash(image)
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

def main():
    # Load Excel and verify columns
    df = pd.read_excel(EXCEL_PATH)
    expected_columns = ['Product ID', 'Front Image', 'Back Image', 'Front side']
    print("📄 Excel columns:", df.columns.tolist())

    for col in expected_columns:
        if col not in df.columns:
            raise ValueError(f"Missing expected column: '{col}' in Excel")

    products = []
    for _, row in df.iterrows():
        pid = str(row['Product ID']).strip()
        products.append((pid, row.get('Front Image'), row.get('Back Image'), row.get('Front side')))

    print(f"✅ Loaded {len(products)} products")

    # Compute reference hashes
    reference_hashes = defaultdict(list)
    for pid, front, back, side in products:
        for label, img_col in zip(['f', 'b', 's'], [front, back, side]):
            if pd.notna(img_col):
                ref_path = os.path.join(IMAGES_FOLDER, str(img_col).strip())
                if os.path.exists(ref_path):
                    h = compute_hash(ref_path)
                    if h:
                        reference_hashes[pid].append((h, label))
                else:
                    print(f"⚠️ Missing reference image: {ref_path}")

    print(f"🔍 Reference hashes loaded for {len(reference_hashes)} products")

    # List all images in the folder
    all_images = [f for f in os.listdir(IMAGES_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"📷 Found {len(all_images)} local images to scan")

    mapping = defaultdict(list)

    for img in tqdm(all_images):
        img_path = os.path.join(IMAGES_FOLDER, img)
        h = compute_hash(img_path)
        if h is None:
            continue

        closest_matches = []
        for pid, refs in reference_hashes.items():
            for ref_hash, label in refs:
                dist = h - ref_hash
                if dist < THRESHOLD:
                    closest_matches.append((pid, label, dist))

        if not closest_matches:
            print(f"🚫 No match for {img}")
            continue

        # Group by Product ID
        grouped = defaultdict(list)
        for pid, label, _ in closest_matches:
            grouped[pid].append(label)

        if len(grouped) == 1:
            pid, labels = list(grouped.items())[0]
            if len(labels) == 1:
                mapping[img].append(pid)
            else:
                mapping[img].extend([f"{pid}-{label}" for label in labels])
        else:
            for pid, labels in grouped.items():
                mapping[img].extend([f"{pid}-{label}" for label in labels])

    # Save result
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, 'w') as f:
        for k, v in mapping.items():
            f.write(f"{k} -> {v}\n")

    print(f"\n✅ Matching complete. Results saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
