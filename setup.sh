#!/bin/bash

# Exit on error
set -e

# Check if python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Exiting."
    exit 1
fi

# Create input directory if it doesn't exist
if [ ! -d "input" ]; then
    mkdir input
    echo "Created input directory."
else
    echo "input directory already exists. Skipping."
fi

# Create output/extracted_images directory if it doesn't exist
if [ ! -d "output/extracted_images" ]; then
    mkdir -p output/extracted_images
    echo "Created output/extracted_images directory."
else
    echo "output/extracted_images directory already exists. Skipping."
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "REFERENCE_DIR=input/<your_dir>" > .env
    echo "QUERY_DIR=output/extracted_images" >> .env
    echo "OUTPUT_PATH=output/output_mapping.xlsx" >> .env
    echo "EXCEL_FILE=input/<your-excel>" >> .env
    echo "OUTPUT_FOLDER=output/extracted_images" >> .env
    echo ".env file created. Please update <your_dir> and <your-excel> as needed."
else
    echo ".env file already exists. Skipping."
fi

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping pip install."
fi

