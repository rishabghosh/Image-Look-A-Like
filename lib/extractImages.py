import openpyxl
import os
import pandas as pd

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
        # Check if a back image exists for this product_id
        back_image_exists = False
        for other_img in ws._images:
            other_anchor = other_img.anchor._from
            other_col, other_row = other_anchor.col + 1, other_anchor.row + 1
            other_image_type = get_image_type(other_col)
            other_product_id = ws.cell(row=other_row, column=COL_INDEX['productId']).value
            if other_product_id == product_id and other_image_type == 'backImage':
                back_image_exists = True
                break
        if image_type == 'frontImage':
            if back_image_exists:
                image_filename = f"{product_id}-f.png"
            else:
                image_filename = f"{product_id}.png"
        elif image_type == 'backImage':
            image_filename = f"{product_id}-b.png"
        elif image_type == 'sideImage' or image_type == 'frontSide':
            image_filename = f"{product_id}-s.png"
        else:
            image_filename = f"{product_id}_{image_type}.png"
        image_path = os.path.join(output_folder, image_filename)
        with open(image_path, "wb") as f:
            f.write(img_data)

        product_map[product_id][image_type] = image_filename

    print("✅ Image mapping written to product_image_mapping.json")

    # After processing images, write output Excel with renamed columns
    output_excel_path = os.path.join(output_folder, 'extracted_images.xlsx')
    rows = []
    for product_id, images in product_map.items():
        row = {
            'this is product Id from EXCEL_FILE': product_id,
            'QUERY_DIR': images.get('frontImage', ''),
            'REFERENCE_DIR': images.get('backImage', ''),
            'reference image name in drive': images.get('frontSide', '')
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_excel(output_excel_path, index=False)
    print(f"✅ Output Excel with renamed columns written to {output_excel_path}")
