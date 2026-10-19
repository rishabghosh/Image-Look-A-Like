import os
import json
import shutil
import pandas as pd
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

def rename_excel_columns(excel_path):
    df = pd.read_excel(excel_path)
    column_map = {
        "product Id": "this is product Id from EXCEL_FILE",
        "image from sheet": "QUERY_DIR",
        "reference image from drive": "REFERENCE_DIR",
        "image name from drive": "REFERENCE_DIR",
        # "reference image name in drive": "reference image name in drive", # keep as is
    }
    df.rename(columns=column_map, inplace=True)
    # Ensure "reference image name in drive" column exists
    if "reference image name in drive" not in df.columns:
        df["reference image name in drive"] = ""
    df.to_excel(excel_path, index=False)
    print("Excel columns renamed.")

if __name__ == "__main__":
    rename_images(REFERENCE_DIR, MAPPING_FILE)
    excel_mapping_path = os.path.join("output", "output_mapping.xlsx")
    if os.path.exists(excel_mapping_path):
        rename_excel_columns(excel_mapping_path)
