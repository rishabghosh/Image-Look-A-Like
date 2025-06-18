# I/O utilities
import os
import csv

def list_image_files(directory, exts={'.png', '.jpg', '.jpeg'}):
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in exts]

def write_output_mapping(output_path, mapping):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['query_image', 'reference_image', 'similarity'])
        for row in mapping:
            writer.writerow(row)

