import argparse
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import re

# --- Argument parsing ---
parser = argparse.ArgumentParser(description="Pretty print a HealthBench example to markdown.")
parser.add_argument("prompt_id", type=str, help="Prompt ID of the example to print.")
parser.add_argument("--dataset", type=str, default="default", choices=["default", "hard", "consensus"], help="Dataset type (default, hard, consensus)")
args = parser.parse_args()

# --- Paths ---
repo_root = Path(__file__).resolve().parent.parent
processed_dir = repo_root / 'processed_data' / args.dataset
output_dir = Path(__file__).parent / 'printed_examples'
output_dir.mkdir(exist_ok=True)

# --- Find the example ---
examples = []
for file in processed_dir.glob("*_example_*.json"):
    df = pd.read_json(file, typ='series')
    examples.append(df.to_dict())

example = next((ex for ex in examples if ex.get('prompt_id') == args.prompt_id), None)
if not example:
    print(f"Error: Example with prompt_id '{args.prompt_id}' not found in dataset '{args.dataset}'.")
    exit(1)

# --- Metadata ---
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
theme = next((tag[6:] for tag in example.get('example_tags', []) if tag.startswith('theme:')), 'Unknown')
physician_category = next((tag[len('physician_agreed_category:'):] for tag in example.get('example_tags', []) if tag.startswith('physician_agreed_category:')), 'Unknown')
dataset = args.dataset

# --- Conversation formatting ---
prompt_data = example.get('prompt', [])
chat_lines = []
for msg in prompt_data:
    role = msg.get('role', '').capitalize()
    content = msg.get('content', '').replace('\n', ' ')
    chat_lines.append(f"| **{role}** | {content} |")
chat_md = "| **Role** | **Message** |\n|---|---|\n" + "\n".join(chat_lines)

# --- Rubric formatting ---
rubrics = example.get('rubrics', [])
# Group by axis
axis_map = {}
for r in rubrics:
    axis = None
    for tag in r.get('tags', []):
        if tag.startswith('axis:'):
            axis = tag.split(':', 1)[1]
            break
    axis = axis or 'Unspecified'
    axis_map.setdefault(axis, []).append(r)

rubric_md = ""
for axis, group in axis_map.items():
    rubric_md += f"\n### Axis: {axis}\n"
    for r in group:
        criterion = r.get('criterion', '')
        points = r.get('points', 0)
        color = '#4ade80' if points >= 0 else '#f87171'
        rubric_md += f"- **{criterion}**  "
        rubric_md += f"<span style='color:{color};font-weight:bold;'>{points:+} pts</span>\n"

# --- Markdown output ---
md = f"""# Example: {args.prompt_id}
**Theme:** {theme}  
**Physician Category:** {physician_category}  
**Dataset:** {dataset}  
**Generated:** {timestamp}

---

## Conversation

{chat_md}

---

## Rubric Criteria
{rubric_md}
---
"""

# --- Save file ---
safe_theme = re.sub(r'[^a-zA-Z0-9_\-]', '_', theme)[:30]
safe_id = args.prompt_id[:12]
safe_time = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{safe_id}_{safe_theme}_{safe_time}.md"
filepath = output_dir / filename
with open(filepath, 'w') as f:
    f.write(md)
print(f"Markdown saved to {filepath}") 