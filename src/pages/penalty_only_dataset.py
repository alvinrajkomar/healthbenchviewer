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
# Try to use display_rubric_criteria for a consistent look
rubrics = []
if 'negative_rubrics' in current_example and isinstance(current_example['negative_rubrics'], list):
    # If negative_rubrics is already a list of dicts
    rubrics = current_example['negative_rubrics']
elif 'negative_rubrics_with_points' in current_example and current_example['negative_rubrics_with_points']:
    # Try to parse the string into rubric dicts (assumes format: criterion (points) | ...)
    import re
    parts = [p.strip() for p in current_example['negative_rubrics_with_points'].split('|')]
    for part in parts:
        m = re.match(r"(.+?)\s*\(([-\d]+)\)$", part)
        if m:
            criterion = m.group(1).strip()
            points = int(m.group(2))
            rubrics.append({'criterion': criterion, 'points': points, 'tags': []})
        elif part:
            rubrics.append({'criterion': part, 'points': -1, 'tags': []})

if rubrics:
    current_example['rubrics'] = rubrics
    st.subheader("Negative Rubric Criteria")
    display_rubric_criteria(current_example, sort_by='axis', show_details=True, show_positive=False, show_negative=True)
else:
    st.info("No negative rubric criteria found in this example.")

# Show penalty metrics
st.subheader("Penalty Metrics")
st.markdown(f"**Total Penalty:** {current_example.get('total_penalty', 0)}")
st.markdown(f"**Penalty Count:** {current_example.get('penalty_count', 0)}") 