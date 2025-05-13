# HealthBench

A repository for processing and analyzing health benchmark data.

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

## Usage

### Data Processing

To download and process the data, run:
```bash
python scripts/download_and_process.py [--dataset {default,hard,consensus}]
```

This will:
1. Download the raw data from the source URL
2. Save it to the `raw_data` directory
3. Process the data and save the results to the `processed_data` directory

Available datasets:
- `default`: The standard HealthBench dataset (default)
- `hard`: The hard version of the HealthBench dataset
- `consensus`: The consensus version of the HealthBench dataset

The processed data will be split into individual JSON files for easier analysis.

### Data Viewer

To start the Streamlit data viewer:
```bash
streamlit run src/viewer.py
```

This will:
1. Start a local web server
2. Open your default web browser to the application
3. Allow you to interactively explore the processed data

## Directory Structure

- `raw_data/`: Contains the downloaded raw data
- `processed_data/`: Contains the processed data files
- `scripts/`: Contains the processing scripts
  - `download_and_process.py`: Downloads and processes the data
  - `process_data.py`: Processes the raw data into individual files
- `src/`: Contains the Streamlit application code
  - `viewer.py`: Main Streamlit application

## Repository Structure

```
healthbench/
├── raw_data/          # Raw data files
├── processed_data/    # Processed data files
├── scripts/           # Data processing scripts
├── src/              # Streamlit application code
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

[Add your license here] 