import streamlit as st
from pathlib import Path

def load_markdown_content(page_name: str) -> str:
    content_path = Path(__file__).parent / 'content' / f'{page_name}.md'
    if content_path.exists():
        with open(content_path, 'r') as f:
            return f.read()
    return ""

st.set_page_config(page_title="HealthBench Viewer", page_icon="🏥", layout="wide")

st.title("HealthBench Dataset")

st.markdown("""
## Welcome to the HealthBench Viewer!

This app allows you to:
- **Explore multiple HealthBench datasets** (Default, Hard, Consensus) with a user-friendly interface
- **Browse and filter examples** by dataset and theme
- **View detailed conversations, ideal completions, and rubric criteria** for each example
- **Download processed data and CSVs** for further analysis

### How to use this app
1. **Select a dataset** using the sidebar (Default, Hard, or Consensus)
2. **Choose a theme** to filter examples, or pick 'Random' for a sample
3. **Navigate through examples** using the Next/Previous buttons
4. **View details** such as the conversation, ideal completion, and rubric breakdown
5. Use the **All Examples** page for a table view of all available examples

_This tool is designed to help researchers, clinicians, and developers explore and analyze HealthBench data efficiently._
""")

st.markdown(load_markdown_content("intro")) 