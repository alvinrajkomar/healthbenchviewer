#!/usr/bin/env python3
"""
Data processing script for HealthBench.
This script processes raw data files and prepares them for analysis or visualization.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
import logging
import argparse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_jsonl_file(file_path: Path) -> List[Dict[str, Any]]:
    """Load a JSONL file and return a list of dictionaries."""
    try:
        data = []
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    data.append(json.loads(line))
        return data
    except Exception as e:
        logger.error(f"Error loading {file_path}: {str(e)}")
        raise

def process_data(data: List[Dict[str, Any]], num_examples: int) -> List[Dict[str, Any]]:
    """
    Process the loaded data and return a subset of examples.
    Args:
        data: List of dictionaries from JSONL file
        num_examples: Number of examples to process
    """
    return data[:num_examples]

def save_json_files(data: List[Dict[str, Any]], output_dir: Path, base_filename: str):
    """Save each example as a separate JSON file."""
    for i, example in enumerate(data):
        output_file = output_dir / f"{base_filename}_example_{i+1}.json"
        with open(output_file, 'w') as f:
            json.dump(example, f, indent=2)
        logger.info(f"Saved example {i+1} to {output_file}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process JSONL files into individual JSON files')
    parser.add_argument('--num_examples', type=int, default=30,
                      help='Number of examples to process (default: 30)')
    args = parser.parse_args()

    # Define paths
    raw_data_dir = Path(__file__).parent.parent / 'raw_data'
    output_dir = Path(__file__).parent.parent / 'processed_data'
    output_dir.mkdir(exist_ok=True)

    # Process each JSONL file in the raw_data directory
    for jsonl_file in raw_data_dir.glob('*.jsonl'):
        logger.info(f"Processing {jsonl_file.name}")
        
        # Load and process data
        data = load_jsonl_file(jsonl_file)
        processed_data = process_data(data, args.num_examples)
        
        # Save processed data as individual JSON files
        save_json_files(processed_data, output_dir, jsonl_file.stem)
        logger.info(f"Processed {len(processed_data)} examples from {jsonl_file.name}")

if __name__ == "__main__":
    main() 