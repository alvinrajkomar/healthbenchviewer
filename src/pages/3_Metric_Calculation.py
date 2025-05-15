import streamlit as st
from pathlib import Path

def load_markdown_content(page_name: str) -> str:
    content_path = Path(__file__).parent.parent / 'content' / f'{page_name}.md'
    if content_path.exists():
        with open(content_path, 'r') as f:
            return f.read()
    return ""

st.title("Metric Calculation")
st.markdown(load_markdown_content("metric_calculation")) 