import pandas as pd
import json
from pathlib import Path

# --- Load the consensus JSONL file ---
jsonl_path = Path('raw_data') / 'healthbench_consensus_data.jsonl'
rows = []
with open(jsonl_path, 'r') as f:
    for line in f:
        data = json.loads(line)
        theme = None
        physician_category = None
        tags = data.get('example_tags', [])
        for tag in tags:
            if tag.startswith('theme:'):
                theme = tag.split('theme:')[1]
            if tag.startswith('physician_agreed_category:'):
                physician_category = tag.split('physician_agreed_category:')[1]
        rubrics = data.get('rubrics', [])
        for rubric in rubrics:
            criterion = rubric.get('criterion', '')
            points = rubric.get('points', None)
            rows.append({
                'theme': theme,
                'physician_category': physician_category,
                'criterion': criterion,
                'points': points
            })
df = pd.DataFrame(rows)
print('Sample of extracted DataFrame:')
print(df.head())

# --- Descriptive statistics ---
print('\nDescriptive statistics:')
print('Number of rubric rows:', len(df))
print('Number of unique (theme, physician_category, criterion, points) rows:', df.drop_duplicates().shape[0])
print('Number of unique criteria:', df["criterion"].nunique())
print('Number of unique themes:', df["theme"].nunique())
print('Number of unique physician categories:', df["physician_category"].nunique())
print(df.describe(include='all'))

# --- View all unique rows (expecting 34) ---
unique_df = df.drop_duplicates().reset_index(drop=True)
print(f'\nUnique rows: {len(unique_df)}')
print(unique_df)

# --- Group unique rows by theme and physician_category, then save ---
grouped_unique_df = unique_df.sort_values(['theme', 'physician_category']).reset_index(drop=True)
grouped_unique_csv_path = Path('notebooks') / 'consensus_criteria_unique.csv'
grouped_unique_df.to_csv(grouped_unique_csv_path, index=False)
print(f'Grouped unique rows saved to {grouped_unique_csv_path.resolve()}') 