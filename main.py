import os
from dotenv import load_dotenv
from lib.core import match_images
import shutil

if __name__ == "__main__":
    load_dotenv()
    reference_dir = os.getenv("REFERENCE_DIR", "input/cartoon")
    query_dir = os.getenv("QUERY_DIR", "output/extracted_images")
    output_path = os.getenv("OUTPUT_PATH", "output/output_mapping.csv")

    # Remove all files from output/extracted_images
    if os.path.exists(query_dir):
        for filename in os.listdir(query_dir):
            file_path = os.path.join(query_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # Call extractImages.py
    import runpy
    runpy.run_path('lib/extractImages.py')

    match_images(reference_dir, query_dir, output_path)
