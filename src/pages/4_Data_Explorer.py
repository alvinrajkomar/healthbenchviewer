import streamlit as st
from utils import (
    get_all_examples,
    display_conversation,
    display_ideal_completion,
    display_rubric_criteria,
    calculate_points_metrics,
    display_points_metrics
)

st.title("Data Explorer")

examples = get_all_examples()
if not examples:
    st.error("No examples found in the processed_data directory.")
else:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Explorer Options")
    example_names = [f"Example {i+1}" for i in range(len(examples))]
    selected_example = st.sidebar.selectbox(
        "Select an example:",
        example_names,
        help="Choose an example to view"
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Display Options")
    sort_by = st.sidebar.radio(
        "Sort criteria by:",
        ["axis", "points"],
        help="Choose how to sort the rubric criteria"
    )
    show_details = st.sidebar.checkbox(
        "Show detailed criteria",
        value=True,
        help="Toggle the visibility of detailed criteria information"
    )
    example_index = int(selected_example.split()[1]) - 1
    example = examples[example_index]
    display_conversation(example)
    display_ideal_completion(example)
    st.markdown("---")
    display_rubric_criteria(example, sort_by, show_details)
    st.markdown("---")
    metrics = calculate_points_metrics(example.get('rubrics', []))
    display_points_metrics(metrics) 