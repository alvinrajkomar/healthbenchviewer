import pandas as pd
import json
from pathlib import Path

def create_penalty_dataset():
    """Create a dataset containing only penalty rubrics from the default dataset."""
    # Read the default dataset
    jsonl_path = Path('raw_data') / 'healthbench_default_data.jsonl'
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
            
            # Extract rubrics and points, but only keep negative ones
            rubrics = data.get('rubrics', [])
            negative_rubrics = []
            negative_points = []
            
            for rubric in rubrics:
                criterion = rubric.get('criterion', '')
                points = rubric.get('points', None)
                if points is not None and points < 0:  # Only keep negative points
                    negative_rubrics.append(criterion)
                    negative_points.append(points)
            
            # Only add to dataset if there are negative rubrics
            if negative_rubrics:
                # Combine rubrics and points into a single string
                rubrics_with_points = ' | '.join([f"{text} ({points})" for text, points in zip(negative_rubrics, negative_points)])
                
                # Calculate penalty metrics
                total_penalty = sum(negative_points)
                penalty_count = len(negative_points)
                
                rows.append({
                    'example_id': example_id,
                    'theme': theme,
                    'physician_category': physician_category,
                    'example': example,
                    'prompt': prompt,
                    'negative_rubrics_with_points': rubrics_with_points,
                    'all_tags': ', '.join(tags),
                    'total_penalty': total_penalty,
                    'penalty_count': penalty_count,
                    'negative_rubrics': negative_rubrics,
                    'negative_points': negative_points
                })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(rows)
    output_path = Path('notebooks') / 'penalty_only_dataset.csv'
    df.to_csv(output_path, index=False)
    
    # Print summary statistics
    print(f"\nPenalty Dataset Summary:")
    print(f"Total examples with penalties: {len(df):,}")
    print(f"Total unique penalty rubrics: {df['penalty_count'].sum():,}")
    print(f"Average penalties per example: {df['penalty_count'].mean():.2f}")
    print(f"Average total penalty per example: {df['total_penalty'].mean():.2f}")
    print(f"Range of penalties: {df['total_penalty'].min()} to {df['total_penalty'].max()}")
    print(f"\nDataset saved to: {output_path}")

if __name__ == '__main__':
    create_penalty_dataset() 