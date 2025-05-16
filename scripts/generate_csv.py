"""
Generate a CSV from the HealthBench JSONL data file.

This is a utility script that provides a simple way to generate CSV files from existing JSONL files.
While download_and_process.py handles the full pipeline (download, process, and CSV generation),
this script is useful when you:
- Already have JSONL files and just want to generate CSVs
- Want to generate CSVs from different JSONL files without downloading
- Need a simpler, single-purpose tool for CSV generation

Usage:
    python scripts/generate_csv.py [input_jsonl_path] [output_csv_path]

- By default, reads from raw_data/healthbench_default_data.jsonl
- By default, writes to processed_data/healthbench_default_data.csv
- Processes all rows in the JSONL file.

Example:
    python scripts/generate_csv.py
    python scripts/generate_csv.py raw_data/healthbench_default_data.jsonl processed_data/healthbench_default_data.csv
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.utils import jsonl_to_dataframe

def main():
    # Default input and output paths
    input_path = Path("raw_data/healthbench_default_data.jsonl")
    output_path = Path("processed_data/healthbench_default_data.csv")

    # Allow optional CLI override
    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])

    print(f"Loading data from: {input_path}")
    df = jsonl_to_dataframe(str(input_path))
    print(f"Saving CSV to: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Done! Saved {len(df)} rows.")

if __name__ == "__main__":
    main() 