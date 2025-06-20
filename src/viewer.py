#!/usr/bin/env python3
"""
Data viewer for HealthBench evaluation data.
Provides an interactive interface to view conversations and rubric criteria.
"""

import streamlit as st
import json
from pathlib import Path
import pandas as pd
from typing import Dict, List, Any
import plotly.express as px

# Custom CSS for better presentation
st.set_page_config(
    page_title="HealthBench Viewer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stMarkdown {
        font-size: 1.1rem;
    }
    h1 {
        color: #2563eb;
        font-size: 2.5rem !important;
        margin-bottom: 2rem !important;
    }
    h2 {
        color: #1e40af;
        font-size: 2rem !important;
        margin-top: 2rem !important;
    }
    h3 {
        color: #1e40af;
        font-size: 1.5rem !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
    }
    .stButton>button:hover {
        background-color: #1e40af;
    }
</style>
""", unsafe_allow_html=True)

def load_json_file(file_path: Path) -> Dict[str, Any]:
    """Load a single JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def get_all_examples() -> List[Dict[str, Any]]:
    """Load all example JSON files from the processed_data directory."""
    data_dir = Path(__file__).parent.parent / 'processed_data'
    examples = []
    for json_file in sorted(data_dir.glob('*_example_*.json')):
        examples.append(load_json_file(json_file))
    return examples

def display_conversation(example: Dict[str, Any]):
    """Display the conversation in a chat-like interface from the 'prompt' field."""
    st.subheader("Conversation")
    
    conversation = example.get('prompt', [])
    if not conversation:
        st.warning("No conversation found in this example.")
        return

    chat_css = """
    <style>
    .chat-container { display: flex; flex-direction: column; gap: 0.5rem; }
    .chat-bubble {
        max-width: 70%;
        padding: 0.75rem 1rem;
        border-radius: 1.2rem;
        margin-bottom: 0.2rem;
        font-size: 1.1rem;
        line-height: 1.5;
        word-break: break-word;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .user-bubble {
        align-self: flex-end;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-bottom-right-radius: 0.3rem;
    }
    .assistant-bubble {
        align-self: flex-start;
        background: #f3f4f6;
        color: #222;
        border-bottom-left-radius: 0.3rem;
    }
    .role-label {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.1rem;
        opacity: 0.7;
    }
    </style>
    """
    st.markdown(chat_css, unsafe_allow_html=True)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for turn in conversation:
        role = turn.get('role', 'unknown')
        content = turn.get('content', '')
        if role.lower() == 'user':
            bubble_class = 'chat-bubble user-bubble'
            role_label = 'User'
        elif role.lower() == 'assistant':
            bubble_class = 'chat-bubble assistant-bubble'
            role_label = 'Assistant'
        else:
            bubble_class = 'chat-bubble assistant-bubble'
            role_label = role.capitalize()
        html = f'''
        <div class="{bubble_class}">
            <div class="role-label">{role_label}</div>
            {content}
        </div>
        '''
        st.markdown(html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def display_ideal_completion(example: Dict[str, Any]):
    """Display the ideal completion if it exists."""
    ideal_completions_data = example.get('ideal_completions_data')
    if ideal_completions_data and isinstance(ideal_completions_data, dict):
        ideal_completion = ideal_completions_data.get('ideal_completion')
        if ideal_completion:
            st.subheader("Ideal Completion")
            st.markdown(ideal_completion)

def extract_axis(tags):
    if not isinstance(tags, list):
        return ''
    for tag in tags:
        if tag.startswith('axis:'):
            return tag.split(':', 1)[1]
    return ''

def get_points_badge_color(points: int) -> str:
    """Return a badge color (hex) for the points value, saturating at +/-10."""
    capped = max(min(points, 10), -10)
    if capped > 0:
        # Muted green
        return '#4ade80'  # green-300
    elif capped < 0:
        # Muted red
        return '#f87171'  # red-400
    else:
        # Neutral gray
        return '#a1a1aa'  # zinc-400

def axis_display_name(axis: str) -> str:
    if not axis:
        return 'Unspecified'
    return axis.replace('_', ' ').capitalize()

def display_rubric_criteria(example: Dict[str, Any], sort_by: str = "axis", show_details: bool = True):
    """Display and sort rubric criteria from the 'rubrics' field."""
    st.subheader("Rubric Criteria")
    
    # Extract criteria and scores
    rubrics = example.get('rubrics', [])
    if not rubrics:
        st.warning("No rubric criteria found in this example.")
        return
    
    # Convert to DataFrame for sorting
    df = pd.DataFrame([
        {
            'criterion': r.get('criterion', ''),
            'points': r.get('points', 0),
            'axis': extract_axis(r.get('tags', [])),
            'tags': r.get('tags', []),
        }
        for r in rubrics
    ])
    
    def colored_header(criterion, points):
        badge_color = get_points_badge_color(points)
        html = f'''
        <div style="display:flex;align-items:center;gap:1rem;background:#18181b;padding:0.7rem 1.2rem;border-radius:0.7rem;margin-bottom:0.2rem;">
            <span style="flex:1;font-weight:600;font-size:1.1rem;color:#fff;">{criterion}</span>
            <span style="background:{badge_color};color:#18181b;padding:0.3rem 0.9rem;border-radius:1.2rem;font-weight:700;font-size:1.05rem;box-shadow:0 1px 4px rgba(0,0,0,0.10);min-width:60px;text-align:center;">{points} pts</span>
        </div>
        '''
        st.markdown(html, unsafe_allow_html=True)
    
    if sort_by == "axis":
        # Group by axis, sort within each axis by points descending
        for axis, group in df.groupby('axis'):
            st.markdown(f"### Axis: {axis if axis else 'Unspecified'}")
            group_sorted = group.sort_values(by="points", ascending=False)
            for _, row in group_sorted.iterrows():
                colored_header(row['criterion'], row['points'])
                if show_details:
                    with st.expander("Details"):
                        st.markdown(f"**Axis:** {row['axis']}")
                        st.markdown(f"**Tags:** {', '.join(row['tags'])}")
    else:
        # Sort the DataFrame
        df = df.sort_values(by=sort_by, ascending=False)
        # Display each criterion
        for _, row in df.iterrows():
            colored_header(row['criterion'], row['points'])
            if show_details:
                with st.expander("Details"):
                    st.markdown(f"**Axis:** {row['axis']}")
                    st.markdown(f"**Tags:** {', '.join(row['tags'])}")

def calculate_points_metrics(rubrics: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate points metrics from rubrics."""
    if not rubrics:
        return {
            'total_actual': 0,
            'max_possible_score': 0,
            'max_possible_penalty': 0,
            'by_axis': {}
        }
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame([
        {
            'criterion': r.get('criterion', ''),
            'points': r.get('points', 0),
            'axis': extract_axis(r.get('tags', [])),
        }
        for r in rubrics
    ])
    
    total_actual = df['points'].sum()
    max_possible_score = df[df['points'] > 0]['points'].sum()
    max_possible_penalty = df[df['points'] < 0]['points'].abs().sum()
    
    # Calculate by axis
    by_axis = {}
    for axis, group in df.groupby('axis'):
        axis_score = group[group['points'] > 0]['points'].sum()
        axis_penalty = group[group['points'] < 0]['points'].abs().sum()
        by_axis[axis] = {
            'max_score': axis_score,
            'max_penalty': axis_penalty
        }
    
    return {
        'total_actual': total_actual,
        'max_possible_score': max_possible_score,
        'max_possible_penalty': max_possible_penalty,
        'by_axis': by_axis
    }

def display_points_metrics(metrics: Dict[str, Any]):
    """Display points metrics in a visually appealing way."""
    st.subheader("Points Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Max Possible Score",
            f"{metrics['max_possible_score']}"
        )
    with col2:
        st.metric(
            "Max Possible Penalty",
            f"{metrics['max_possible_penalty']}"
        )
    
    # Create a DataFrame for the axis breakdown
    axis_data = []
    for axis, data in metrics['by_axis'].items():
        axis_data.append({
            'Category': axis_display_name(axis),
            'Max Score': data['max_score'],
            'Max Penalty': data['max_penalty']
        })
    df = pd.DataFrame(axis_data)
    
    st.markdown("### Points by Category")
    if not df.empty:
        # Use lighter color gradients and add padding/border radius for a modern look
        styler = (
            df.style
            .background_gradient(subset=["Max Score"], cmap="BuGn", vmin=0, vmax=max(df["Max Score"].max(), 1), gmap=None, axis=None)
            .background_gradient(subset=["Max Penalty"], cmap="OrRd", vmin=0, vmax=max(df["Max Penalty"].max(), 1), gmap=None, axis=None)
            .set_properties(**{
                'border-radius': '10px',
                'padding': '8px',
                'border': '1px solid #222',
                'font-size': '1.1em',
            })
            .format(precision=0)
        )
        st.write(styler)
    else:
        st.dataframe(df, use_container_width=True)

def load_markdown_content(page_name: str) -> str:
    """Load markdown content from the content directory."""
    content_path = Path(__file__).parent / 'content' / f'{page_name}.md'
    if content_path.exists():
        with open(content_path, 'r') as f:
            return f.read()
    return ""

def display_page_content(page_name: str):
    """Display the content for a specific page."""
    content = load_markdown_content(page_name)
    if content:
        st.markdown(content)
    else:
        st.error(f"Content not found for {page_name}")

def main():
    PAGES = {
        "Introduction": "intro",
        "Example Generation": "example_generation",
        "Rubric Generation": "rubric_generation",
        "Metric Calculation": "metric_calculation",
        "Data Explorer": "data_explorer"
    }

    st.sidebar.title("HealthBench Viewer")

    # Use a selectbox for navigation
    page = st.sidebar.selectbox(
        "Navigation",
        list(PAGES.keys()),
        index=list(PAGES.keys()).index(st.session_state.get("page", "Introduction"))
    )
    st.session_state.page = page

    # --- PAGE LOGIC ---
    if page == "Introduction":
        st.title("HealthBench Dataset")
        display_page_content("intro")
    elif page == "Example Generation":
        st.title("Example Generation")
        display_page_content("example_generation")
    elif page == "Rubric Generation":
        st.title("Rubric Generation")
        display_page_content("rubric_generation")
    elif page == "Metric Calculation":
        st.title("Metric Calculation")
        display_page_content("metric_calculation")
    else:  # Data Explorer
        st.title("Data Explorer")
        
        # Get all examples
        examples = get_all_examples()
        if not examples:
            st.error("No examples found in the processed_data directory.")
            return
        
        # Move all options to sidebar
        st.sidebar.markdown("---")
        st.sidebar.subheader("Data Explorer Options")
        
        # Example selector in sidebar
        example_names = [f"Example {i+1}" for i in range(len(examples))]
        selected_example = st.sidebar.selectbox(
            "Select an example:",
            example_names,
            help="Choose an example to view"
        )
        
        # Display options in sidebar
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
        
        # Get the selected example
        example_index = int(selected_example.split()[1]) - 1
        example = examples[example_index]
        
        # Main content area
        # Display conversation
        display_conversation(example)
        
        # Display ideal completion
        display_ideal_completion(example)
        
        # Display rubric criteria
        st.markdown("---")
        display_rubric_criteria(example, sort_by, show_details)
        
        # Display points metrics
        st.markdown("---")
        metrics = calculate_points_metrics(example.get('rubrics', []))
        display_points_metrics(metrics)

if __name__ == "__main__":
    main() 