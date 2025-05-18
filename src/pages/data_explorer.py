import streamlit as st
import pandas as pd
from pathlib import Path
from utils import (
    get_all_examples,
    display_conversation,
    display_ideal_completion,
    display_rubric_criteria,
    calculate_points_metrics,
    display_points_metrics,
    create_examples_dataframe
)

st.title("Data Explorer")

# --- Sticky horizontal navigation bar ---
st.markdown("""
<style>
.sticky-nav {
    position: sticky;
    top: 0;
    z-index: 999;
    background: #18181b;
    padding: 0.7rem 0 0.7rem 0;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid #333;
    display: flex;
    gap: 2.5rem;
    justify-content: center;
}
.sticky-nav a {
    color: #3b82f6;
    font-weight: 600;
    text-decoration: none;
    font-size: 1.1rem;
    transition: color 0.2s;
}
.sticky-nav a:hover {
    color: #ef4444;
    text-decoration: underline;
}
</style>
<div class="sticky-nav">
  <a href="#select-theme">Select Theme</a>
  <a href="#examples">Examples</a>
  <a href="#conversation">Conversation</a>
  <a href="#rubric-criteria">Rubric Criteria</a>
  <a href="#points-analysis">Points Analysis</a>
</div>
""", unsafe_allow_html=True)

# Dataset selection in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Dataset Selection")
dataset_type = st.sidebar.selectbox(
    "Select Dataset",
    ["default", "hard", "consensus"],
    format_func=lambda x: x.capitalize(),
    help="Choose which dataset to explore"
)

# Robust repo root detection
repo_root = Path(__file__).resolve().parent.parent.parent
data_dir = repo_root / 'processed_data' / dataset_type
examples = get_all_examples(data_dir)

if not examples:
    st.error(f"No examples found in the {dataset_type} dataset.")
else:
    # Create DataFrame for initial view and theme selection
    df = create_examples_dataframe(examples)
    
    # Create a mapping of IDs to examples for quick lookup
    example_map = {example.get('prompt_id', f'example_{i+1}'): example for i, example in enumerate(examples)}
    
    # --- Anchor: Select Theme ---
    st.markdown('<a name="select-theme"></a>', unsafe_allow_html=True)
    st.markdown("---")
    st.header("Select Theme")

    def prettify_theme(theme):
        return theme.replace("_", " ").title()
    themes = sorted(df['Theme'].unique().tolist())
    theme_options = ['Random'] + themes
    # Set a robust default theme
    default_theme = 'Emergency Referrals' if 'Emergency Referrals' in themes else (themes[0] if themes else 'Random')
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = default_theme
        if default_theme == 'Random':
            st.session_state.current_examples = df.sample(n=min(10, len(df))).reset_index(drop=True)
        else:
            filtered_df = df[df['Theme'] == default_theme]
            st.session_state.current_examples = filtered_df.sample(n=min(10, len(filtered_df))).reset_index(drop=True)
        st.session_state.current_index = 0
    # Two-row grid CSS (tight)
    st.markdown("""
        <style>
        .theme-btn button {
            min-width: 90px;
            max-width: 150px;
            margin: 0.08rem 0.18rem 0.08rem 0;
            padding: 0.13rem 0.4rem;
            border-radius: 3px !important;
            border: 1px solid #2563eb !important;
            background: #18181b !important;
            color: #fff !important;
            font-size: 0.89rem !important;
            font-weight: 500 !important;
            transition: background 0.2s, color 0.2s;
        }
        .theme-btn button.selected-theme-btn {
            border: 2px solid #ef4444 !important;
            color: #ef4444 !important;
            font-weight: 700 !important;
        }
        .theme-btn button:hover {
            background: #2563eb !important;
            color: #fff !important;
        }
        </style>
    """, unsafe_allow_html=True)
    # Display theme buttons in two rows, each button is clickable and highlighted if selected
    n = len(theme_options)
    split = (n + 1) // 2
    row1 = theme_options[:split]
    row2 = theme_options[split:]
    for row in [row1, row2]:
        cols = st.columns(len(row))
        for idx, theme in enumerate(row):
            with cols[idx]:
                is_selected = (theme == st.session_state.selected_theme)
                btn_label = prettify_theme(theme) if theme != "Random" else "Random"
                btn_key = f"theme_{theme}"
                if st.button(btn_label, key=btn_key, use_container_width=True):
                    st.session_state.selected_theme = theme
                    if theme == 'Random':
                        st.session_state.current_examples = df.sample(n=10).reset_index(drop=True)
                    else:
                        filtered_df = df[df['Theme'] == theme]
                        st.session_state.current_examples = filtered_df.sample(n=min(10, len(filtered_df))).reset_index(drop=True)
                    st.session_state.current_index = 0
                # Add a marker div for JS/CSS to target the selected button
                if is_selected:
                    st.markdown(f"""
                        <style>
                        [data-testid="stButton"][key="{btn_key}"] button {{
                            border: 2px solid #ef4444 !important;
                            color: #ef4444 !important;
                            font-weight: 700 !important;
                        }}
                        </style>
                    """, unsafe_allow_html=True)

    # --- Anchor: Examples ---
    st.markdown('<a name="examples"></a>', unsafe_allow_html=True)
    st.markdown("---")
    st.header(f"Examples in {dataset_type.capitalize()} Dataset")

    # Display options (keep in sidebar)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Display Options")
    sort_by = st.sidebar.radio(
        "Sort criteria by:",
        ["axis", "points"],
        help="Choose how to sort the rubric criteria"
    )
    show_details = st.sidebar.checkbox(
        "Show detailed criteria",
        value=False,
        help="Toggle the visibility of detailed criteria information"
    )
    show_ideal_completion = st.sidebar.checkbox(
        "Show ideal completion",
        value=True,
        help="Toggle the visibility of the ideal completion"
    )

    # Main content area
    if len(st.session_state.current_examples) > 0:
        # Navigation controls
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("Previous", disabled=st.session_state.current_index == 0):
                st.session_state.current_index = max(0, st.session_state.current_index - 1)
        with col2:
            st.markdown(f"### Example {st.session_state.current_index + 1} of {len(st.session_state.current_examples)}")
        with col3:
            if st.button("Next", disabled=st.session_state.current_index == len(st.session_state.current_examples) - 1):
                st.session_state.current_index = min(len(st.session_state.current_examples) - 1, st.session_state.current_index + 1)
        
        # Get current example
        current_example_id = st.session_state.current_examples.iloc[st.session_state.current_index]['ID']
        current_example = example_map.get(current_example_id)
        
        if current_example:
            # --- Anchor: Conversation ---
            st.markdown('<a name="conversation"></a>', unsafe_allow_html=True)
            st.markdown("---")
            # Show theme above conversation
            theme = current_example.get('example_tags', [])
            theme_str = next((tag[6:] for tag in theme if tag.startswith('theme:')), None)
            if theme_str:
                st.markdown(f"<div style='font-size:1.1rem;font-weight:600;color:#2563eb;margin-bottom:0.3rem;'>Theme: {theme_str.replace('_', ' ').title()}</div>", unsafe_allow_html=True)
            display_conversation(current_example)
            if show_ideal_completion:
                display_ideal_completion(current_example)
            # --- Anchor: Rubric Criteria ---
            st.markdown('<a name="rubric-criteria"></a>', unsafe_allow_html=True)
            st.markdown("---")
            display_rubric_criteria(current_example, sort_by, show_details)
            # --- Anchor: Points Analysis ---
            st.markdown('<a name="points-analysis"></a>', unsafe_allow_html=True)
            st.markdown("---")
            metrics = calculate_points_metrics(current_example.get('rubrics', []))
            display_points_metrics(metrics)
        else:
            st.error(f"Could not find example with ID: {current_example_id}")
    else:
        st.info("No examples available to display.") 