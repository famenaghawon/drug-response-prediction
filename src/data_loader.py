import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.multitest import multipletests
import os

DATA_DIR = "data/raw"

def load_gdsc_data():
    """Loads real GDSC data. Assumes files are in data/raw."""
    try:
        # Load drug response (IC50)
        response_file = os.path.join(DATA_DIR, "GDSC2_fitted_dose_response.xlsx")
        df_resp = pd.read_excel(response_file)
        
        # Load expression data (assuming a simplified CSV for the repo)
        # In a real scenario, you'd parse the larger RData or CSV.
        expr_file = os.path.join(DATA_DIR, "Expression_Data.csv") 
        df_expr = pd.read_csv(expr_file, index_col=0) # Genes x Cell Lines
        
        return df_resp, df_expr
    except FileNotFoundError:
        st.error("Data files not found. Please run download_data.py")
        return None, None

def preprocess_data(df_resp, df_expr):
    """Merges data, calculates FDR, and selects top features."""
    # Transpose expression so rows are Cell Lines, cols are Genes
    df_expr_t = df_expr.T 
    
    # Merge on Cell Line Name (COSMIC ID or Cell Line Name)
    # Ensure column names match between datasets (e.g., 'Cell Line Name')
    merged = pd.merge(df_resp, df_expr_t, left_on='CELL_LINE_NAME', right_index=True, how='inner')
    
    # --- REAL STATISTICS ---
    # Calculate correlation between gene expression and IC50 for a specific drug
    # This replaces the "fake p-values"
    drug_name = 'Erlotinib' # Example
    drug_df = merged[merged['DRUG_NAME'] == drug_name]
    
    if drug_df.empty:
        return None, None, None
        
    gene_cols = df_expr_t.columns
    ic50 = drug_df['LN_IC50']
    
    correlations = {}
    p_values = {}
    
    for gene in gene_cols:
        # Pearson correlation
        corr, p = stats.pearsonr(drug_df[gene], ic50)
        correlations[gene] = corr
        p_values[gene] = p
        
    # FDR Correction (Multiple testing correction - CRITICAL for research)
    p_vals = list(p_values.values())
    reject, p_adj, _, _ = multipletests(p_vals, alpha=0.05, method='fdr_bh')
    
    results_df = pd.DataFrame({
        'Gene': gene_cols,
        'Correlation': correlations.values(),
        'P_Value_Raw': p_vals,
        'P_Value_FDR': p_adj,
        'Significant': reject
    }).sort_values('Correlation', ascending=False)
    
    return drug_df, results_df, gene_cols

def get_ml_features(results_df, top_n=50):
    """Returns top N significant genes for the ML model."""
    sig_genes = results_df[results_df['Significant']]['Gene'].head(top_n).tolist()
    if len(sig_genes) < 5:
        # Fallback to top correlations if FDR finds nothing (common in small samples)
        sig_genes = results_df['Gene'].head(top_n).tolist()
    return sig_genes
