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

def display_rubric_criteria(example: Dict[str, Any]):
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
    
    # Add sorting options
    sort_by = st.selectbox(
        "Sort criteria by:",
        ["points", "axis", "criterion"],
        index=0
    )
    
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
                with st.expander("Details"):
                    st.markdown(f"**Axis:** {row['axis']}")
                    st.markdown(f"**Tags:** {', '.join(row['tags'])}")
    else:
        # Sort the DataFrame
        df = df.sort_values(by=sort_by, ascending=False)
        # Display each criterion
        for _, row in df.iterrows():
            colored_header(row['criterion'], row['points'])
            with st.expander("Details"):
                st.markdown(f"**Axis:** {row['axis']}")
                st.markdown(f"**Tags:** {', '.join(row['tags'])}")

def main():
    st.set_page_config(page_title="HealthBench Data Viewer", layout="wide")
    st.title("HealthBench Data Viewer")
    
    # Load all examples
    examples = get_all_examples()
    
    if not examples:
        st.error("No examples found in the processed_data directory. Please run the data processing script first:")
        st.code("python scripts/download_and_process.py")
        return
    
    # Sidebar for example selection and display options
    st.sidebar.title("Navigation")
    example_names = [f"Example {i+1}" for i in range(len(examples))]
    selected_example = st.sidebar.selectbox(
        "Select an example:",
        example_names,
        index=0
    )
    
    # Display options
    st.sidebar.markdown("---")
    st.sidebar.subheader("Display Options")
    show_score_distribution = st.sidebar.toggle(
        "Show Score Distribution",
        value=True,
        help="Toggle the visibility of the criteria score distribution chart"
    )
    
    # Get the selected example
    example_index = int(selected_example.split()[-1]) - 1
    example = examples[example_index]
    
    # Conversation at the top (full width)
    display_conversation(example)
    
    # Display ideal completion if it exists
    display_ideal_completion(example)
    
    st.markdown("---")
    
    # Criteria Score Distribution (full width) - only if enabled
    if show_score_distribution:
        st.subheader("Criteria Score Distribution")
        rubrics = example.get('rubrics', [])
        if rubrics:
            df = pd.DataFrame([
                {
                    'criterion': r.get('criterion', ''),
                    'points': r.get('points', 0),
                    'axis': extract_axis(r.get('tags', [])),
                }
                for r in rubrics
            ])
            fig = px.bar(
                df,
                x='criterion',
                y='points',
                color='axis',
                title="Points by Criterion",
                labels={'criterion': 'Criterion', 'points': 'Points'},
                height=400
            )
            fig.update_layout(
                legend=dict(
                    orientation='v',
                    yanchor='top',
                    y=1,
                    xanchor='left',
                    x=1.02,
                    font=dict(size=18),
                    bgcolor='rgba(0,0,0,0)'
                )
            )
            fig.update_xaxes(showticklabels=False, title=None)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")
    
    # Rubric criteria (full width)
    display_rubric_criteria(example)

if __name__ == "__main__":
    main() 