#!/usr/bin/env python3
"""
Data download and processing script for HealthBench.
This script downloads the raw data, processes it, and generates CSV files.
"""

import requests
from pathlib import Path
import logging
import json
import pandas as pd
from typing import Dict, List, Any
import argparse
from enum import Enum
import sys

# Add src to path for importing utils
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.utils import jsonl_to_dataframe

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatasetType(Enum):
    DEFAULT = "default"
    HARD = "hard"
    CONSENSUS = "consensus"

DATASET_URLS = {
    DatasetType.DEFAULT: "https://openaipublic.blob.core.windows.net/simple-evals/healthbench/2025-05-07-06-14-12_oss_eval.jsonl",
    DatasetType.HARD: "https://openaipublic.blob.core.windows.net/simple-evals/healthbench/hard_2025-05-08-21-00-10.jsonl",
    DatasetType.CONSENSUS: "https://openaipublic.blob.core.windows.net/simple-evals/healthbench/consensus_2025-05-09-20-00-46.jsonl"
}

def download_data(url: str, output_path: Path) -> None:
    """Download data from URL and save to file."""
    try:
        logger.info(f"Downloading data from {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save the data
        with open(output_path, 'wb') as f:
            f.write(response.content)
        logger.info(f"Data downloaded successfully to {output_path}")
    except Exception as e:
        logger.error(f"Error downloading data: {str(e)}")
        raise

def process_and_save_data(jsonl_file: Path, output_dir: Path, base_filename: str, num_examples: int = None):
    """Process the JSONL file and save both individual JSON files and CSV."""
    # Load and process data
    data = []
    with open(jsonl_file, 'r') as f:
        for i, line in enumerate(f):
            if num_examples is not None and i >= num_examples:
                break
            if line.strip():
                data.append(json.loads(line))
    
    # Save individual JSON files
    for i, example in enumerate(data):
        output_file = output_dir / f"{base_filename}_example_{i+1}.json"
        with open(output_file, 'w') as f:
            json.dump(example, f, indent=2)
        logger.info(f"Saved example {i+1} to {output_file}")
    
    # Generate and save CSV
    df = jsonl_to_dataframe(str(jsonl_file))
    if num_examples is not None:
        df = df.head(num_examples)
    csv_file = output_dir / f"{base_filename}.csv"
    df.to_csv(csv_file, index=False)
    logger.info(f"Saved CSV file to {csv_file}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download and process HealthBench datasets')
    parser.add_argument('--dataset', 
                      type=str,
                      choices=[d.value for d in DatasetType] + ['all'],
                      default='all',
                      help='Dataset to download (default: all)')
    parser.add_argument('--num_examples', 
                      type=int,
                      default=None,
                      help='Number of examples to process (default: all)')
    args = parser.parse_args()

    # Define paths
    base_dir = Path(__file__).parent.parent
    raw_data_dir = base_dir / 'raw_data'
    processed_data_dir = base_dir / 'processed_data'
    
    # Determine which datasets to process
    if args.dataset == 'all':
        datasets_to_process = list(DatasetType)
    else:
        datasets_to_process = [DatasetType(args.dataset)]
    
    # Process each dataset
    for dataset_type in datasets_to_process:
        logger.info(f"\nProcessing {dataset_type.value} dataset...")
        
        # Get URL and set output filename
        input_url = DATASET_URLS[dataset_type]
        output_file = raw_data_dir / f"healthbench_{dataset_type.value}_data.jsonl"
        
        # Download the data
        download_data(input_url, output_file)
        
        # Create dataset-specific output directory
        output_dir = processed_data_dir / dataset_type.value
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Process and save the data
        process_and_save_data(
            output_file, 
            output_dir, 
            output_file.stem,
            args.num_examples
        )
        
        logger.info(f"Completed processing {dataset_type.value} dataset!")
    
    logger.info("\nAll data download and processing completed successfully!")

if __name__ == "__main__":
    main() 