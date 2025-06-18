# Configuration/constants
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

REFERENCE_DIR = 'input/cartoon'
QUERY_DIR = 'output/extracted_images'
OUTPUT_PATH = 'output/output_mapping.csv'

