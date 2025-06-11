
# image_product_mapper

This project maps local images to their respective product IDs from an Excel sheet.

## Features

- Matches front, back, and front-side images using image similarity.
- Renames images according to the product ID and type.
- Outputs a CSV with the mapping: `original_filename -> [mapped_tags]`

## Usage

1. Place the Excel file in the root directory.
2. Place all images in an `images/` folder.
3. Run `main.py` to generate `output_mapping.csv`.

## Setup

```bash
pip install -r requirements.txt
python main.py
```
