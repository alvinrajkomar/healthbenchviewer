# HealthBench Viewer

A web app for exploring and analyzing HealthBench datasets.

## What is this app?

**HealthBench Viewer** is a user-friendly Streamlit application that allows you to:
- **Explore multiple HealthBench datasets** (Default, Hard, Consensus)
- **Browse and filter examples** by dataset and theme
- **View detailed conversations, ideal completions, and rubric criteria** for each example
- **Download processed data and CSVs** for further analysis

This tool is designed for researchers, clinicians, and developers who want to interactively explore HealthBench data.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Data Processing

The `download_and_process.py` script automates the process of downloading, processing, and organizing HealthBench datasets. By default, it will download and process **all three datasets** (`default`, `hard`, and `consensus`), generating both individual JSON files and a CSV for each dataset.

**Basic usage (downloads and processes all datasets):**
```bash
python scripts/download_and_process.py
```

**To specify a single dataset:**
```bash
python scripts/download_and_process.py --dataset hard
```
Options for `--dataset` are: `default`, `hard`, `consensus`, or `all` (all is the default).

**To limit the number of examples processed (optional):**
```bash
python scripts/download_and_process.py --dataset consensus --num_examples 100
```
This will only process the first 100 examples from the consensus dataset.

**What happens when you run the script:**
- Downloads the raw data for the selected dataset(s)
- Saves the raw data in the `raw_data/` directory
- Processes the data and saves individual JSON files in `processed_data/<dataset>/`
- Generates a CSV file for each dataset in its respective folder

**Example output:**
- `processed_data/default/healthbench_default_data.csv`
- `processed_data/hard/healthbench_hard_data.csv`
- `processed_data/consensus/healthbench_consensus_data.csv`
- Plus many individual JSON files for each example

Available datasets:
- `default`: The standard HealthBench dataset
- `hard`: The hard version of the HealthBench dataset
- `consensus`: The consensus version of the HealthBench dataset
- `all`: Download and process all datasets

## Launching the Data Viewer

To start the Streamlit data viewer:
```bash
streamlit run src/Home.py
```

This will:
1. Start a local web server
2. Open your default web browser to the application
3. Allow you to interactively explore the processed data

### How to use the app
1. **Select a dataset** using the sidebar (Default, Hard, or Consensus)
2. **Choose a theme** to filter examples, or pick 'Random' for a sample
3. **Navigate through examples** using the Next/Previous buttons
4. **View details** such as the conversation, ideal completion, and rubric breakdown

## Directory Structure

- `raw_data/`: Contains the downloaded raw data
- `processed_data/`: Contains the processed data files, organized by dataset type
- `scripts/`: Contains the processing scripts
  - `download_and_process.py`: Downloads and processes the data
- `src/`: Contains the Streamlit application code
  - `Home.py`: Main Streamlit application (entry point)
  - `pages/4_Data_Explorer.py`: Data Explorer page
  - `utils.py`: Utility functions for data loading and processing
- `requirements.txt`: Python dependencies
- `README.md`: This file

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

[Add your license here] 