import streamlit as st
import pandas as pd
from pathlib import Path
from utils import display_conversation, display_rubric_criteria, calculate_points_metrics, display_points_metrics

st.title("Penalty Only Dataset")

# Load the penalty dataset
penalty_path = Path(__file__).resolve().parent.parent.parent / 'outputs' / 'analysis' / 'penalty_only_dataset.csv'
if not penalty_path.exists():
    st.error("Penalty Only dataset file not found. Please run the analysis scripts first.")
    st.stop()

# Load as DataFrame and convert to list of dicts for navigation
penalty_df = pd.read_csv(penalty_path)
examples = penalty_df.to_dict(orient='records')

# Theme selection
themes = sorted(set([ex.get('theme', '') for ex in examples if pd.notna(ex.get('theme', ''))]))
default_theme = themes[0] if themes else None
st.sidebar.subheader("Theme Filter")
selected_theme = st.sidebar.selectbox("Select Theme", ["All"] + themes, index=0)

# Filter examples by theme
if selected_theme != "All":
    filtered_examples = [ex for ex in examples if ex.get('theme', '') == selected_theme]
else:
    filtered_examples = examples

if not filtered_examples:
    st.info("No examples available for the selected theme.")
    st.stop()

# Navigation
if 'penalty_example_index' not in st.session_state:
    st.session_state.penalty_example_index = 0

max_index = len(filtered_examples) - 1
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("Previous", disabled=st.session_state.penalty_example_index == 0):
        st.session_state.penalty_example_index = max(0, st.session_state.penalty_example_index - 1)
with col2:
    st.markdown(f"### Example {st.session_state.penalty_example_index + 1} of {len(filtered_examples)}")
with col3:
    if st.button("Next", disabled=st.session_state.penalty_example_index == max_index):
        st.session_state.penalty_example_index = min(max_index, st.session_state.penalty_example_index + 1)

current_example = filtered_examples[st.session_state.penalty_example_index]

# Show theme above conversation
if current_example.get('theme'):
    st.markdown(f"<div style='font-size:1.1rem;font-weight:600;color:#2563eb;margin-bottom:0.3rem;'>Theme: {current_example['theme'].replace('_', ' ').title()}</div>", unsafe_allow_html=True)

# Show conversation (prompt)
prompt = current_example.get('prompt', '')
if prompt:
    st.subheader("Conversation")
    st.markdown(f"<div style='background:#23232b;padding:1rem;border-radius:0.7rem;margin-bottom:1rem;'>{prompt.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
else:
    st.info("No conversation found in this example.")

# Show rubric criteria (negative rubrics)
negative_rubrics = current_example.get('negative_rubrics_with_points', '')
if negative_rubrics:
    st.subheader("Negative Rubric Criteria")
    st.markdown(f"<div style='background:#18181b;padding:0.7rem 1.2rem;border-radius:0.7rem;margin-bottom:0.2rem;color:#ef4444;font-weight:600;'>{negative_rubrics}</div>", unsafe_allow_html=True)
else:
    st.info("No negative rubric criteria found in this example.")

# Show penalty metrics
st.subheader("Penalty Metrics")
st.markdown(f"**Total Penalty:** {current_example.get('total_penalty', 0)}")
st.markdown(f"**Penalty Count:** {current_example.get('penalty_count', 0)}") 