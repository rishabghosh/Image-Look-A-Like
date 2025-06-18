import os
from dotenv import load_dotenv
from lib.core import match_images
from lib.extractImages import extract_images
import shutil

if __name__ == "__main__":
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
    reference_dir = os.getenv("REFERENCE_DIR")
    query_dir = os.getenv("QUERY_DIR")
    output_path = os.getenv("OUTPUT_PATH")
    excel_file = os.getenv("EXCEL_FILE")
    output_folder = os.getenv("OUTPUT_FOLDER")

    # Remove all files from output/extracted_images
    if os.path.exists(output_folder):
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # Call extract_images with env values
    extract_images(excel_file, output_folder)

    match_images(reference_dir, query_dir, output_path)
