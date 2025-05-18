import streamlit as st
from pathlib import Path

st.title("Main Analysis")

# Load the markdown content from the analysis output
analysis_path = Path(__file__).resolve().parent.parent.parent / 'outputs' / 'analysis' / 'computed_basic_analysis_default.md'
if analysis_path.exists():
    with open(analysis_path, 'r') as f:
        content = f.read()
    st.markdown(content)
else:
    st.error("Analysis file not found. Please run the analysis scripts first.") 