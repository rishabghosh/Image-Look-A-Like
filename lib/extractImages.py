import openpyxl
import os

COL_INDEX = {
    'productId': 1,
    'frontImage': 2,
    'backImage': 3,
    'frontSide': 4
}


def get_image_type(col):
    if col == COL_INDEX['frontImage']:
        return 'frontImage'
    elif col == COL_INDEX['backImage']:
        return 'backImage'
    elif col == COL_INDEX['frontSide']:
        return 'frontSide'
    return None


def extract_images(excel_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Load workbook
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active

    # Initialize map
    product_map = {}

    # Extract image data with anchor
    for img in ws._images:
        # Get cell position from anchor (e.g., B2)
        anchor = img.anchor._from
        col, row = anchor.col + 1, anchor.row + 1  # 1-based indexing

        image_type = get_image_type(col)
        if not image_type:
            continue  # not a relevant column

        product_id = ws.cell(row=row, column=COL_INDEX['productId']).value
        if not product_id:
            continue

        if product_id not in product_map:
            product_map[product_id] = {}

        # Save image to disk
        img_data = img._data()
        image_filename = f"{product_id}_{image_type}.png"
        image_path = os.path.join(output_folder, image_filename)
        with open(image_path, "wb") as f:
            f.write(img_data)

        product_map[product_id][image_type] = image_filename

    print("✅ Image mapping written to product_image_mapping.json")
