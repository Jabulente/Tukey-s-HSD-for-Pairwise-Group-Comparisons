# **Tukey's Honest Significant Difference (THSD)**  

Tukey's Honest Significant Difference (THSD) test is a post-hoc statistical analysis used to compare all possible group means after rejecting the null hypothesis in ANOVA. It controls the family-wise error rate, making it ideal for identifying which specific groups differ significantly in multi-group experiments. In this project, THSD is applied to evaluate disease resistance across eggplant varieties, providing pairwise comparisons of infection severity, wilt index, plant height, and survival rate with adjusted confidence intervals and p-values.  

The implementation follows a structured workflow: (1) data preparation with target metrics and grouping variables, (2) automated THSD execution via `pairwise_tukeyhsd`, and (3) results formatted for clarity—highlighting significant differences (α=0.05) with asterisks and 95% CIs. This approach ensures rigorous, reproducible comparisons while minimizing Type I errors.  

---

### **Structured Implementation**  

#### **1. Data Requirements**  
```python
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Define target metrics and grouping column
METRICS = ['Infection Severity (%)', 'Wilt index', 'Plant height (cm)', 'Survival rate (%)']
GROUP_COL = 'Variety'
```

#### **2. THSD Execution Function**  
```python
def run_thsd(dataframe: pd.DataFrame, metrics: list, group_column: str) -> pd.DataFrame:
    """
    Performs THSD tests for specified metrics across groups.
    Returns DataFrame with Diff (marked if significant), p-value, and CI.
    """
    results = []
    for metric in metrics:
        thsd_result = pairwise_tukeyhsd(
            endog=dataframe[metric],
            groups=dataframe[group_column],
            alpha=0.05
        )
        # Parse results table (skip header row [0])
        for row in thsd_result.summary().data[1:]:
            diff = float(row[2])
            is_sig = row[6]  # True if p < 0.05
            results.append({
                'Metric': metric,
                'Group1': row[0],
                'Group2': row[1],
                'Diff': f"{diff:.1f}*" if is_sig else f"{diff:.1f}",
                'p-value': f"{float(row[3]):.4f}",
                'CI': f"[{float(row[4]):.1f}, {float(row[5]):.1f}]"
            })
    return pd.DataFrame(results)
```

#### **3. Output Example**  
| Metric               | Group1    | Group2    | Diff  | p-value   | 95% CI        |  
|----------------------|-----------|-----------|-------|-----------|---------------|  
| `Wilt index`         | Variety_A | Variety_B | `2.3*`| `0.0012`  | `[1.5, 3.1]`  |  

**Key**:  
- `*` = Significant (p < 0.05)  
- **CI** = Confidence Interval of mean difference  

#### **4. Execution**  
```python
df = pd.read_csv("Eggplant_Fusarium_Fertilizer_Data.csv")
thsd_results = run_thsd(df, METRICS, GROUP_COL)
thsd_results.to_csv("THSD_Results.csv", index=False)
```

---

**Why This Structure?**  
- **Clarity**: Separates data input, analysis, and output.  
- **Reproducibility**: Self-contained function with typed parameters.  
- **Actionable Results**: Directly highlights significant comparisons.  
