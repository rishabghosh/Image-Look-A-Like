import os
import csv

DEFAULT_IMAGE_EXTS = {'.png', '.jpg', '.jpeg'}
OUTPUT_MAPPING_HEADER = ['query_image', 'reference_image', 'similarity']

def list_image_files(directory, exts=DEFAULT_IMAGE_EXTS):
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in exts]

def write_output_mapping(output_path, mapping):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(OUTPUT_MAPPING_HEADER)
        for row in mapping:
            writer.writerow(row)
