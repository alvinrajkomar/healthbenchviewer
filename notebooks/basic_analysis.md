# HealthBench Dataset Analysis

This document provides a basic analysis of both the default and consensus datasets from HealthBench.

## Dataset Overview

### Default Dataset
- **Total Examples**: 5,000
- **Unique Themes**: 7
- **Unique Physician Categories**: 17

### Consensus Dataset
- **Total Examples**: 3,671
- **Unique Themes**: 7
- **Unique Physician Categories**: 17

## Points Analysis

### Default Dataset
- **Range**: 3 to 230 points
- **Mean**: 52.18 points
- **Standard Deviation**: 28.19 points
- **Distribution**:
  - 161 unique point values
  - Most common values are distributed across a wide range
  - Shows high variability in scoring

### Consensus Dataset
- **Range**: 10 to 15 points
- **Mean**: 10.97 points
- **Standard Deviation**: 1.98 points
- **Distribution**:
  - Only 2 unique values: 10 (2,960 examples) and 15 (711 examples)
  - Much more standardized scoring

## Penalties Analysis

### Default Dataset
- **Range**: -124 to 0 points
- **Mean**: -24.08 points
- **Standard Deviation**: 16.03 points
- **Distribution**:
  - 99 unique penalty values
  - 319 examples have no penalty (0)
  - Shows significant variation in penalties

### Consensus Dataset
- **All Examples**: 0 penalty points
- No negative points present

## Rubric Count Analysis

### Default Dataset
- **Range**: 2 to 48 rubrics
- **Mean**: 11.45 rubrics
- **Standard Deviation**: 5.70 rubrics
- **Distribution**:
  - Most common: 11 rubrics (409 examples)
  - Wide distribution across many values
  - Shows high complexity in evaluation

### Consensus Dataset
- **Range**: 2 to 3 rubrics
- **Mean**: 2.19 rubrics
- **Standard Deviation**: 0.40 rubrics
- **Distribution**:
  - Only 2 values: 2 rubrics (2,960 examples) and 3 rubrics (711 examples)
  - Much simpler evaluation structure

## Positive/Negative Rubric Analysis

### Default Dataset
#### Positive Rubrics
- **Range**: 1 to 33 rubrics
- **Mean**: 7.93 rubrics
- **Distribution**: Wide spread across many values

#### Negative Rubrics
- **Range**: 0 to 18 rubrics
- **Mean**: 3.52 rubrics
- **Distribution**: 
  - 319 examples have no negative rubrics
  - Most common: 3 negative rubrics (1,049 examples)

### Consensus Dataset
#### Positive Rubrics
- Exactly matches rubric count
- 2 positive rubrics (2,960 examples)
- 3 positive rubrics (711 examples)

#### Negative Rubrics
- All examples have 0 negative rubrics

## Correlations

### Default Dataset
- Strong positive correlation (0.93) between max_points and rubric_count
- Strong negative correlation (-0.95) between max_penalty and negative_rubric_count
- Strong positive correlation (0.97) between max_points and positive_rubric_count

### Consensus Dataset
- Perfect correlation (1.0) between:
  - max_points and rubric_count
  - max_points and positive_rubric_count
  - rubric_count and positive_rubric_count

## Key Insights

1. **Dataset Complexity**:
   - Default dataset shows much higher complexity with:
     - Wider range of points
     - More rubrics per example
     - Presence of penalties
     - More varied scoring patterns
   - Consensus dataset is more standardized with:
     - Limited point values
     - Fewer rubrics
     - No penalties
     - Consistent scoring patterns

2. **Evaluation Structure**:
   - Default dataset appears to use a more granular and complex evaluation system
   - Consensus dataset uses a simplified, binary-like evaluation system

3. **Scoring Patterns**:
   - Default dataset shows more nuanced scoring with both positive and negative points
   - Consensus dataset focuses only on positive points with a very limited range

4. **Data Distribution**:
   - Default dataset shows more natural distribution of scores and rubrics
   - Consensus dataset shows a more artificial, clustered distribution 