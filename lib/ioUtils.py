import os
import openpyxl

DEFAULT_IMAGE_EXTS = {'.png', '.jpg', '.jpeg'}
OUTPUT_MAPPING_HEADER = ['query_image', 'reference_image', 'similarity']

def list_image_files(directory, exts=DEFAULT_IMAGE_EXTS):
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in exts]

def write_output_mapping(output_path, mapping):
    if output_path.endswith('.csv'):
        output_path = output_path[:-4] + '.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(OUTPUT_MAPPING_HEADER)
    for row in mapping:
        ws.append(row)
    wb.save(output_path)
