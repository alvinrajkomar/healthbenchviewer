#!/usr/bin/env python3
"""
Data download and processing script for HealthBench.
This script downloads the raw data from the provided URL and processes it.
"""

import requests
from pathlib import Path
import logging
import subprocess
import sys
import argparse
from enum import Enum

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

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download and process HealthBench datasets')
    parser.add_argument('--dataset', 
                      type=str,
                      choices=[d.value for d in DatasetType],
                      default=DatasetType.DEFAULT.value,
                      help='Dataset to download (default: default)')
    args = parser.parse_args()

    # Convert string argument to enum
    dataset_type = DatasetType(args.dataset)
    
    # Define paths
    base_dir = Path(__file__).parent.parent
    raw_data_dir = base_dir / 'raw_data'
    raw_data_dir.mkdir(exist_ok=True)
    
    # Get URL and set output filename
    input_url = DATASET_URLS[dataset_type]
    output_file = raw_data_dir / f"healthbench_{dataset_type.value}_data.jsonl"
    
    # Download the data
    download_data(input_url, output_file)
    
    # Run the processing script
    logger.info("Running data processing script...")
    process_script = base_dir / "scripts" / "process_data.py"
    subprocess.run([sys.executable, str(process_script)], check=True)
    
    logger.info("Data download and processing completed successfully!")

if __name__ == "__main__":
    main() 