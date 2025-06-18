# Image Product Mapper

## Overview
This project maps product images to reference images using CLIP embeddings and supports extracting images from Excel files. All input/output paths and configuration are managed via environment variables in a `.env` file.

## Setup
1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables:**
   - Copy or edit the provided `.env` file in the project root:
     ```env
     REFERENCE_DIR=input/cartoon
     QUERY_DIR=output/extracted_images
     OUTPUT_PATH=output/output_mapping.csv
     EXCEL_FILE=input/cartoon.xlsx
     OUTPUT_FOLDER=output/extracted_images
     ```
   - All paths are controlled from this file. No paths are hardcoded in the codebase.

## Usage
Run the main script:
```bash
python main.py
```

This will:
1. Clean the `OUTPUT_FOLDER` directory.
2. Extract images from the Excel file specified by `EXCEL_FILE` into `OUTPUT_FOLDER`.
3. Map query images (`QUERY_DIR`) to reference images (`REFERENCE_DIR`) and write the results to `OUTPUT_PATH`.

## Project Structure
- `main.py` — Entry point. Loads all configuration from `.env` and orchestrates the workflow.
- `lib/` — Contains all core logic as reusable modules.
- `.env` — All input/output paths and configuration.
- `requirements.txt` — Python dependencies.

## Notes
- Make sure your `.env` file is up to date and contains all required variables.
- No path variables are hardcoded or independently declared in the codebase; all are loaded from `.env` and passed as parameters.
