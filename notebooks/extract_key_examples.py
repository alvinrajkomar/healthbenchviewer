import pandas as pd
import json
from pathlib import Path
import argparse
from datetime import datetime

def generate_analysis_markdown(df, dataset_type, dataset_path, output_name):
    """Generate markdown analysis of the dataset and save to file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def median_iqr(series):
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        return f"{series.median():.2f} ({q1:.2f}–{q3:.2f})"
    
    markdown_template = f"""# HealthBench Dataset Analysis
Generated on: {timestamp}
Dataset: {dataset_type}
Path: {dataset_path}

## Dataset Overview
- **Total Examples**: {len(df):,}
- **Unique Themes**: {df["theme"].nunique()}
- **Unique Physician Categories**: {df["physician_category"].nunique()}

## Points Analysis
- **Range**: {df["max_points"].min()} to {df["max_points"].max()} points
- **Mean (SD)**: {df["max_points"].mean():.2f} ({df["max_points"].std():.2f}) points
- **Median (IQR)**: {median_iqr(df["max_points"])} points
- **Distribution**:
  - {df["max_points"].nunique()} unique point values
  - Most common values: {df["max_points"].value_counts().head(3).to_dict()}

## Penalties Analysis
- **Range**: {df["max_penalty"].min()} to {df["max_penalty"].max()} points
- **Mean (SD)**: {df["max_penalty"].mean():.2f} ({df["max_penalty"].std():.2f}) points
- **Median (IQR)**: {median_iqr(df["max_penalty"])} points
- **Distribution**:
  - {df["max_penalty"].nunique()} unique penalty values
  - {len(df[df["max_penalty"] == 0])} examples have no penalty (0)
  - Most common penalties: {df["max_penalty"].value_counts().head(3).to_dict()}

## Rubric Count Analysis
- **Range**: {df["rubric_count"].min()} to {df["rubric_count"].max()} rubrics
- **Mean (SD)**: {df["rubric_count"].mean():.2f} ({df["rubric_count"].std():.2f}) rubrics
- **Median (IQR)**: {median_iqr(df["rubric_count"])} rubrics
- **Distribution**:
  - Most common: {df["rubric_count"].value_counts().index[0]} rubrics ({df["rubric_count"].value_counts().iloc[0]} examples)
  - Top 3 most common counts: {df["rubric_count"].value_counts().head(3).to_dict()}

## Positive/Negative Rubric Analysis

### Positive Rubrics
- **Range**: {df["positive_rubric_count"].min()} to {df["positive_rubric_count"].max()} rubrics
- **Mean (SD)**: {df["positive_rubric_count"].mean():.2f} ({df["positive_rubric_count"].std():.2f}) rubrics
- **Median (IQR)**: {median_iqr(df["positive_rubric_count"])} rubrics
- **Distribution**: 
  - Most common: {df["positive_rubric_count"].value_counts().index[0]} positive rubrics ({df["positive_rubric_count"].value_counts().iloc[0]} examples)

### Negative Rubrics
- **Range**: {df["negative_rubric_count"].min()} to {df["negative_rubric_count"].max()} rubrics
- **Mean (SD)**: {df["negative_rubric_count"].mean():.2f} ({df["negative_rubric_count"].std():.2f}) rubrics
- **Median (IQR)**: {median_iqr(df["negative_rubric_count"])} rubrics
- **Distribution**: 
  - {len(df[df["negative_rubric_count"] == 0])} examples have no negative rubrics
  - Most common: {df["negative_rubric_count"].value_counts().index[0]} negative rubrics ({df["negative_rubric_count"].value_counts().iloc[0]} examples)

## Key Insights

1. **Dataset Complexity**:
   - Shows {'high' if df["max_points"].nunique() > 10 else 'low'} complexity with:
     - {'Wide' if df["max_points"].max() - df["max_points"].min() > 50 else 'Limited'} range of points
     - {'Many' if df["rubric_count"].max() > 5 else 'Few'} rubrics per example
     - {'Includes' if df["max_penalty"].min() < 0 else 'No'} penalties
     - {'Varied' if df["max_points"].std() > 10 else 'Consistent'} scoring patterns

2. **Evaluation Structure**:
   - Uses a {'granular' if df["rubric_count"].nunique() > 5 else 'simplified'} evaluation system
   - {'Includes' if df["max_penalty"].min() < 0 else 'No'} negative scoring

3. **Scoring Patterns**:
   - {'Shows' if df["max_penalty"].min() < 0 else 'Focuses only on'} positive points
   - {'Wide' if df["max_points"].std() > 10 else 'Limited'} range of possible scores

4. **Data Distribution**:
   - {'Natural' if df["max_points"].nunique() > 10 else 'Artificial'} distribution of scores
   - {'Varied' if df["rubric_count"].nunique() > 5 else 'Clustered'} distribution of rubrics
"""
    analysis_path = Path('notebooks') / output_name
    with open(analysis_path, 'w') as f:
        f.write(markdown_template)
    print(f"Analysis for {dataset_type} saved to {output_name}")

def generate_comparative_analysis(dfs, dataset_types, output_name):
    """Generate comparative analysis between multiple datasets."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    markdown_template = f"""# HealthBench Comparative Dataset Analysis
Generated on: {timestamp}

## Dataset Overview Comparison
| Metric | {' | '.join(dataset_types)} |
|--------|{'|'.join(['---' for _ in dataset_types])}|
| Total Examples | {' | '.join([f"{len(df):,}" for df in dfs])} |
| Unique Themes | {' | '.join([f"{df['theme'].nunique()}" for df in dfs])} |
| Unique Physician Categories | {' | '.join([f"{df['physician_category'].nunique()}" for df in dfs])} |

## Points Analysis Comparison
| Metric | {' | '.join(dataset_types)} |
|--------|{'|'.join(['---' for _ in dataset_types])}|
| Mean Points | {' | '.join([f"{df['max_points'].mean():.2f}" for df in dfs])} |
| Median Points | {' | '.join([f"{df['max_points'].median():.2f}" for df in dfs])} |
| Points Range | {' | '.join([f"{df['max_points'].min()}-{df['max_points'].max()}" for df in dfs])} |
| Points Std Dev | {' | '.join([f"{df['max_points'].std():.2f}" for df in dfs])} |

## Rubric Analysis Comparison
| Metric | {' | '.join(dataset_types)} |
|--------|{'|'.join(['---' for _ in dataset_types])}|
| Mean Rubrics | {' | '.join([f"{df['rubric_count'].mean():.2f}" for df in dfs])} |
| Median Rubrics | {' | '.join([f"{df['rubric_count'].median():.2f}" for df in dfs])} |
| Mean Positive Rubrics | {' | '.join([f"{df['positive_rubric_count'].mean():.2f}" for df in dfs])} |
| Mean Negative Rubrics | {' | '.join([f"{df['negative_rubric_count'].mean():.2f}" for df in dfs])} |

## Penalty Analysis Comparison
| Metric | {' | '.join(dataset_types)} |
|--------|{'|'.join(['---' for _ in dataset_types])}|
| Mean Penalty | {' | '.join([f"{df['max_penalty'].mean():.2f}" for df in dfs])} |
| Median Penalty | {' | '.join([f"{df['max_penalty'].median():.2f}" for df in dfs])} |
| Max Penalty | {' | '.join([f"{df['max_penalty'].max()}" for df in dfs])} |
| Examples with No Penalty | {' | '.join([f"{len(df[df['max_penalty'] == 0])}" for df in dfs])} |

## Key Comparative Insights

1. **Dataset Size and Diversity**:
   - {' | '.join([f"{dataset_types[i]}: {len(dfs[i]):,} examples, {dfs[i]['theme'].nunique()} themes" for i in range(len(dfs))])}
   - {' | '.join([f"{dataset_types[i]}: {dfs[i]['physician_category'].nunique()} physician categories" for i in range(len(dfs))])}

2. **Scoring Complexity**:
   - {' | '.join([f"{dataset_types[i]}: {dfs[i]['max_points'].nunique()} unique point values" for i in range(len(dfs))])}
   - {' | '.join([f"{dataset_types[i]}: {dfs[i]['rubric_count'].nunique()} unique rubric counts" for i in range(len(dfs))])}

3. **Evaluation Structure**:
   - {' | '.join([f"{dataset_types[i]}: {dfs[i]['positive_rubric_count'].mean():.1f} positive rubrics, {dfs[i]['negative_rubric_count'].mean():.1f} negative rubrics" for i in range(len(dfs))])}
   - {' | '.join([f"{dataset_types[i]}: {dfs[i]['max_penalty'].min()} to {dfs[i]['max_penalty'].max()} penalty range" for i in range(len(dfs))])}

4. **Scoring Patterns**:
   - {' | '.join([f"{dataset_types[i]}: {dfs[i]['max_points'].mean():.1f} mean points, {dfs[i]['max_points'].std():.1f} std dev" for i in range(len(dfs))])}
   - {' | '.join([f"{dataset_types[i]}: {dfs[i]['max_points'].max() - dfs[i]['max_points'].min()} point range" for i in range(len(dfs))])}
"""
    analysis_path = Path('notebooks') / output_name
    with open(analysis_path, 'w') as f:
        f.write(markdown_template)
    print(f"Comparative analysis saved to {output_name}")

def main():
    # Process individual datasets
    dfs = []
    dataset_types = ['default', 'consensus', 'hard']
    for dataset_type in dataset_types:
        jsonl_path = Path('raw_data') / f'healthbench_{dataset_type}_data.jsonl'
        rows = []
        with open(jsonl_path, 'r') as f:
            for line in f:
                data = json.loads(line)
                # Extract basic metadata
                theme = None
                physician_category = None
                tags = data.get('example_tags', [])
                for tag in tags:
                    if tag.startswith('theme:'):
                        theme = tag.split('theme:')[1]
                    if tag.startswith('physician_agreed_category:'):
                        physician_category = tag.split('physician_agreed_category:')[1]
                # Extract example content and prompt
                example = data.get('example', '')
                example_id = data.get('example_id', '')
                # Format prompt conversation
                prompt_data = data.get('prompt', [])
                formatted_prompt = []
                for msg in prompt_data:
                    role = msg.get('role', '')
                    content = msg.get('content', '')
                    formatted_prompt.append(f"{role.upper()}: {content}")
                prompt = "\n".join(formatted_prompt)
                # Extract rubrics and points
                rubrics = data.get('rubrics', [])
                rubric_texts = []
                rubric_points = []
                for rubric in rubrics:
                    criterion = rubric.get('criterion', '')
                    points = rubric.get('points', None)
                    rubric_texts.append(criterion)
                    rubric_points.append(points)
                # Combine rubrics and points into a single string
                rubrics_with_points = ' | '.join([f"{text} ({points})" for text, points in zip(rubric_texts, rubric_points)])
                # Calculate new columns
                points_list = [p for p in rubric_points if isinstance(p, (int, float))]
                max_points = sum(p for p in points_list if p is not None and p >= 0)
                max_penalty = sum(p for p in points_list if p is not None and p < 0)
                rubric_count = len(rubric_points)
                positive_rubric_count = sum(1 for p in points_list if p is not None and p >= 0)
                negative_rubric_count = sum(1 for p in points_list if p is not None and p < 0)
                rows.append({
                    'example_id': example_id,
                    'theme': theme,
                    'physician_category': physician_category,
                    'example': example,
                    'prompt': prompt,
                    'rubrics_with_points': rubrics_with_points,
                    'all_tags': ', '.join(tags),
                    'max_points': max_points,
                    'max_penalty': max_penalty,
                    'rubric_count': rubric_count,
                    'positive_rubric_count': positive_rubric_count,
                    'negative_rubric_count': negative_rubric_count
                })
        df = pd.DataFrame(rows)
        dfs.append(df)
        generate_analysis_markdown(df, dataset_type, jsonl_path, f'computed_basic_analysis_{dataset_type}.md')
    
    # Generate comparative analysis
    generate_comparative_analysis(dfs, dataset_types, 'computed_comparative_analysis.md')
    print('\nAll analyses complete!')

if __name__ == '__main__':
    main() 