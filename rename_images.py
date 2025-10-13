import os
import json
import shutil
from dotenv import load_dotenv

load_dotenv()

REFERENCE_DIR = os.getenv("REFERENCE_DIR")
MAPPING_FILE = os.getenv("OUTPUT_JSON")

def rename_images(reference_dir, mapping_file):
    with open(mapping_file, "r") as f:
        mapping = json.load(f)

    for old_name, new_name in mapping.items():
        old_path = os.path.join(reference_dir, old_name)
        new_path = os.path.join(reference_dir, new_name)
        if os.path.exists(old_path):
            shutil.move(old_path, new_path)
            print(f"Renamed: {old_name} -> {new_name}")
        else:
            print(f"File not found: {old_name}")

if __name__ == "__main__":
    rename_images(REFERENCE_DIR, MAPPING_FILE)
