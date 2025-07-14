from statsmodels.stats.multicomp import pairwise_tukeyhsd
import pandas as pd

def perform_tukey_hsd_test(dataframe, metrics, group_column):
    """
    Perform Tukey's HSD test for multiple metrics across specified groups.
    
    Parameters:
    - dataframe: pd.DataFrame containing the data
    - metrics: list of column names to analyze
    - group_column: column name containing the grouping variable
    
    Returns:
    - pd.DataFrame with all pairwise comparison results
    """
    results = []
    
    for metric in metrics:
        # Perform Tukey HSD test for the current metric
        tukey_results = pairwise_tukeyhsd(
            endog=dataframe[metric],
            groups=dataframe[group_column],
            alpha=0.05
        )
        
        # Convert results to a structured format
        summary_table = tukey_results.summary()
        
        # Skip the header row (index 0) and process each comparison
        for row in summary_table.data[1:]:
            results.append({
                'Metric': metric,
                'Group 1': row[0],
                'Group 2': row[1],
                'Mean Difference': row[2],
                'P Value': row[3],
                'CI Lower': row[4],
                'CI Upper': row[5],
                'Significant': row[6]
            })
    
    return pd.DataFrame(results)

# Main execution
if __name__ == "__main__":
    # Load data
    DATA_PATH = "../Datasets/Eggplant Fusarium Fertilizer Data.csv"
    df = pd.read_csv(DATA_PATH)
    
    # Define metrics to analyze
    ANALYSIS_METRICS = [
        'Infection Severity (%)',
        'Wilt index', 
        'Plant height (cm)', 
        'Days to wilt symptoms', 
        'Survival rate (%)', 
        'Disease incidence (%)'
    ]
    
    # Perform analysis
    tukey_results = perform_tukey_hsd_test(
        dataframe=df,
        metrics=ANALYSIS_METRICS,
        group_column='Variety'
    )
    
    # Configure display options
    pd.set_option("display.float_format", "{:.3f}".format)
    
    # Show first 10 results
    display(tukey_results.head(10))
