import streamlit as st
import pandas as pd
from pathlib import Path
import json
from typing import Dict, List, Any

def load_json_file(file_path: Path) -> Dict[str, Any]:
    """Load a single JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def get_all_examples() -> List[Dict[str, Any]]:
    """Load all example JSON files from the processed_data directory."""
    data_dir = Path(__file__).parent.parent.parent / 'processed_data'
    examples = []
    for json_file in sorted(data_dir.glob('*_example_*.json')):
        examples.append(load_json_file(json_file))
    return examples

def extract_axis(tags: List[str]) -> str:
    """Extract the axis from tags."""
    for tag in tags:
        if tag.startswith('axis:'):
            return tag[6:]
    return ""

def format_conversation(prompt: List[Dict[str, str]]) -> str:
    """Format the conversation into a readable string."""
    if not prompt:
        return ""
    formatted = []
    for turn in prompt:
        role = turn.get('role', 'unknown')
        content = turn.get('content', '')
        formatted.append(f"{role.upper()}: {content}")
    return "\n".join(formatted)

def create_examples_dataframe(examples: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create a DataFrame from the examples."""
    rows = []
    for i, example in enumerate(examples):
        # Extract basic information
        prompt_id = example.get('prompt_id', f'example_{i+1}')
        tags = example.get('example_tags', [])
        theme = next((tag[6:] for tag in tags if tag.startswith('theme:')), '')
        physician_category = next((tag[len('physician_agreed_category:'):] for tag in tags if tag.startswith('physician_agreed_category:')), '')
        
        # Extract conversation
        conversation_full = format_conversation(example.get('prompt', []))
        conversation_preview = conversation_full[:500] + ("..." if len(conversation_full) > 500 else "")
        
        # Extract ideal completion with proper null checks
        ideal_completions_data = example.get('ideal_completions_data')
        ideal_completion_full = ''
        if ideal_completions_data and isinstance(ideal_completions_data, dict):
            ideal_completion_full = ideal_completions_data.get('ideal_completion', '')
        ideal_completion_preview = ideal_completion_full[:500] + ("..." if len(ideal_completion_full) > 500 else "")
        
        # Extract rubric information
        rubrics = example.get('rubrics', [])
        total_points = sum(r.get('points', 0) for r in rubrics)
        axes = [extract_axis(r.get('tags', [])) for r in rubrics]
        unique_axes = list(set(axes))
        
        rows.append({
            'ID': prompt_id,
            'Theme': theme,
            'Physician Category': physician_category,
            'Conversation Preview': conversation_preview,
            'Conversation Full': conversation_full,
            'Ideal Completion Preview': ideal_completion_preview,
            'Ideal Completion Full': ideal_completion_full,
            'Total Points': total_points,
            'Axes': ', '.join(unique_axes),
            'Number of Criteria': len(rubrics)
        })
    
    return pd.DataFrame(rows)

st.title("All Examples")

# Get all examples
examples = get_all_examples()
if not examples:
    st.error("No examples found in the processed_data directory.")
else:
    # Create DataFrame
    df = create_examples_dataframe(examples)
    
    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filters")
    
    # Theme filter
    themes = [''] + sorted(df['Theme'].unique().tolist())
    selected_theme = st.sidebar.selectbox(
        "Filter by Theme:",
        themes,
        help="Select a theme to filter examples"
    )
    
    # Physician Category filter
    categories = [''] + sorted(df['Physician Category'].unique().tolist())
    selected_category = st.sidebar.selectbox(
        "Filter by Physician Category:",
        categories,
        help="Select a physician category to filter examples"
    )
    
    # Apply filters
    filtered_df = df.copy()
    if selected_theme:
        filtered_df = filtered_df[filtered_df['Theme'] == selected_theme]
    if selected_category:
        filtered_df = filtered_df[filtered_df['Physician Category'] == selected_category]
    
    # Pagination setup
    PAGE_SIZE = 100
    total_examples = len(filtered_df)
    total_pages = max(1, (total_examples + PAGE_SIZE - 1) // PAGE_SIZE)
    page_num = st.sidebar.number_input(
        "Page number",
        min_value=1,
        max_value=total_pages,
        value=1,
        step=1,
        help=f"Select which page of {PAGE_SIZE} examples to view"
    )
    start_idx = (page_num - 1) * PAGE_SIZE
    end_idx = min(start_idx + PAGE_SIZE, total_examples)
    page_df = filtered_df.iloc[start_idx:end_idx]

    # Display statistics
    st.markdown("### Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Examples", len(filtered_df))
    with col2:
        st.metric("Average Points", f"{filtered_df['Total Points'].mean():.1f}")
    with col3:
        st.metric("Unique Themes", len(filtered_df['Theme'].unique()))
    
    # Display the paginated DataFrame with longer previews using st.data_editor or fallback to dropdown
    st.markdown(f"### Examples (Page {page_num} of {total_pages})")
    editor_df = page_df[[
        'ID', 'Theme', 'Physician Category',
        'Conversation Preview', 'Ideal Completion Preview',
        'Total Points', 'Axes', 'Number of Criteria'
    ]].copy()
    selected_row = None
    try:
        selected = st.data_editor(
            editor_df,
            use_container_width=True,
            column_config={
                "Conversation Preview": st.column_config.TextColumn(
                    "Conversation (Preview)",
                    width="large",
                    help="The conversation between the user and assistant (first 500 chars)"
                ),
                "Ideal Completion Preview": st.column_config.TextColumn(
                    "Ideal Completion (Preview)",
                    width="large",
                    help="The ideal completion for this example (first 500 chars)"
                ),
                "Total Points": st.column_config.NumberColumn(
                    "Total Points",
                    help="Total points for all criteria",
                    format="%d"
                ),
                "Axes": st.column_config.TextColumn(
                    "Axes",
                    help="The axes covered by this example"
                )
            },
            hide_index=True,
            disabled=True,
            key="all_examples_editor",
            num_rows="dynamic",
            selection_mode="single"
        )
        # If selection works, get the selected row
        if selected and selected.get('selected_rows'):
            selected_idx = selected['selected_rows'][0]
            selected_row = page_df.iloc[selected_idx]
    except TypeError:
        # Fallback: show the table and use dropdown for selection
        st.info("Row selection is not supported in your Streamlit version. Please use the dropdown below to select an example.")
        st.dataframe(
            editor_df,
            use_container_width=True,
            hide_index=True
        )
        example_ids = page_df['ID'].tolist()
        if example_ids:
            selected_id = st.selectbox("Select Example ID to view details:", example_ids)
            selected_row = page_df[page_df['ID'] == selected_id].iloc[0]
    
    # Show details for the selected row
    st.markdown("### View Full Conversation and Completion for the Selected Example")
    if selected_row is not None:
        st.markdown(f"**Example ID:** {selected_row['ID']}")
        st.markdown("**Conversation:**")
        st.text(selected_row['Conversation Full'])
        st.markdown("**Ideal Completion:**")
        st.text(selected_row['Ideal Completion Full']) 