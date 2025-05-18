# HealthBench Dataset Analysis
Generated on: 2025-05-18 13:35:13
Dataset: hard
Path: raw_data/healthbench_hard_data.jsonl

## Dataset Overview
- **Total Examples**: 1,000
- **Unique Themes**: 7
- **Unique Physician Categories**: 17

## Points Analysis
- **Range**: 5 to 215 points
- **Mean (SD)**: 51.60 (27.65) points
- **Median (IQR)**: 49.00 (32.00–67.00) points
- **Distribution**:
  - 126 unique point values
  - Most common values: {35: 22, 54: 22, 52: 21}

## Penalties Analysis
- **Range**: -112 to 0 points
- **Mean (SD)**: -29.18 (16.69) points
- **Median (IQR)**: -26.00 (-38.00–-17.00) points
- **Distribution**:
  - 85 unique penalty values
  - 3 examples have no penalty (0)
  - Most common penalties: {-18: 33, -21: 33, -8: 32}

## Rubric Count Analysis
- **Range**: 2 to 40 rubrics
- **Mean (SD)**: 11.85 (5.66) rubrics
- **Median (IQR)**: 11.00 (8.00–15.00) rubrics
- **Distribution**:
  - Most common: 14 rubrics (72 examples)
  - Top 3 most common counts: {14: 72, 12: 69, 10: 67}

## Positive/Negative Rubric Analysis

### Positive Rubrics
- **Range**: 1 to 30 rubrics
- **Mean (SD)**: 7.71 (4.02) rubrics
- **Median (IQR)**: 7.00 (5.00–10.00) rubrics
- **Distribution**: 
  - Most common: 6 positive rubrics (100 examples)

### Negative Rubrics
- **Range**: 0 to 15 rubrics
- **Mean (SD)**: 4.13 (2.26) rubrics
- **Median (IQR)**: 4.00 (2.00–5.00) rubrics
- **Distribution**: 
  - 3 examples have no negative rubrics
  - Most common: 3 negative rubrics (194 examples)

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
