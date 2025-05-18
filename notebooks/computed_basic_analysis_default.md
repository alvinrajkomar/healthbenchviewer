# HealthBench Dataset Analysis
Generated on: 2025-05-18 13:56:58
Dataset: default
Path: raw_data/healthbench_default_data.jsonl

## Dataset Overview
- **Total Examples**: 5,000
- **Unique Themes**: 7
- **Unique Physician Categories**: 17

## Points Analysis
- **Range**: 3 to 230 points
- **Mean (SD)**: 52.18 (28.19) points
- **Median (IQR)**: 51.00 (32.00–68.00) points
- **Distribution**:
  - 161 unique point values
  - Most common values: {10: 303, 52: 95, 57: 85}

## Penalties Analysis
- **Range**: -124 to 0 points
- **Mean (SD)**: -24.08 (16.03) points
- **Median (IQR)**: -22.00 (-33.00–-13.00) points
- **Distribution**:
  - 99 unique penalty values
  - 319 examples have no penalty (0)
  - Most common penalties: {0: 319, -15: 161, -18: 151}

## Rubric Count Analysis
- **Range**: 2 to 48 rubrics
- **Mean (SD)**: 11.45 (5.70) rubrics
- **Median (IQR)**: 11.00 (8.00–15.00) rubrics
- **Distribution**:
  - Most common: 11 rubrics (409 examples)
  - Top 3 most common counts: {11: 409, 12: 375, 13: 371}

## Positive/Negative Rubric Analysis

### Positive Rubrics
- **Range**: 1 to 33 rubrics
- **Mean (SD)**: 7.93 (4.06) rubrics
- **Median (IQR)**: 8.00 (5.00–10.00) rubrics
- **Distribution**: 
  - Most common: 8 positive rubrics (539 examples)

### Negative Rubrics
- **Range**: 0 to 18 rubrics
- **Mean (SD)**: 3.52 (2.19) rubrics
- **Median (IQR)**: 3.00 (2.00–5.00) rubrics
- **Distribution**: 
  - 319 examples have no negative rubrics
  - Most common: 3 negative rubrics (1049 examples)

## Key Insights

1. **Dataset Complexity**:
   - Shows high complexity with:
     - Wide range of points
     - Many rubrics per example
     - Includes penalties
     - Varied scoring patterns

2. **Evaluation Structure**:
   - Uses a granular evaluation system
   - Includes negative scoring

3. **Scoring Patterns**:
   - Shows positive points
   - Wide range of possible scores

4. **Data Distribution**:
   - Natural distribution of scores
   - Varied distribution of rubrics
