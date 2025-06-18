import os
import openpyxl
from openpyxl.drawing.image import Image as OpenpyxlImage
from PIL import Image as PILImage
import json

DEFAULT_IMAGE_EXTS = {'.png', '.jpg', '.jpeg'}
OUTPUT_MAPPING_HEADER = ['query_image', 'reference_image', 'similarity']
IMAGE_SIZE = (80, 80)
IMAGE_COLUMN = 'B'


def list_image_files(directory, exts=DEFAULT_IMAGE_EXTS):
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in exts]

def write_output_mapping(output_path, mapping):
    if output_path.endswith('.csv'):
        output_path = output_path[:-4] + '.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['query_image', 'image', 'reference_image', 'similarity'])
    ws.column_dimensions[IMAGE_COLUMN].width = 15
    extracted_images_dir = os.path.join(os.path.dirname(os.path.dirname(output_path)), 'output', 'extracted_images')
    temp_files = []
    json_data = []
    for row in mapping:
        query_image = row[0]
        col_a = query_image.replace('-frontImage', '-f').replace('-backImage', '-b').replace('-sideImage', '-s')
        image_path = os.path.join(extracted_images_dir, query_image)
        ws.append([col_a, '', row[1], row[2]])
        current_row = ws.max_row
        json_data.append(f"{col_a}: {row[1]}")
        if os.path.exists(image_path):
            temp_path = None
            try:
                with PILImage.open(image_path) as img:
                    img.thumbnail(IMAGE_SIZE)
                    temp_path = image_path + '_temp.png'
                    img.save(temp_path)
                img_for_excel = OpenpyxlImage(temp_path)
                ws.add_image(img_for_excel, f'{IMAGE_COLUMN}{current_row}')
                ws.row_dimensions[current_row].height = 60
                temp_files.append(temp_path)
            finally:
                pass
    wb.save(output_path)
    for temp_path in temp_files:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    # Save col_a:col_c as JSON (as a list of strings)
    json_output_path = os.path.splitext(output_path)[0] + '.json'
    with open(json_output_path, 'w') as jf:
        json.dump(json_data, jf, indent=2)
