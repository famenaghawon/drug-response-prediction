import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import os
from sklearn.model_selection import train_test_split

DATA_DIR = "data/raw"

def load_gdsc_data():
    """Loads real GDSC data and standardizes column names."""
    try:
        response_file = os.path.join(DATA_DIR, "GDSC2_fitted_dose_response_27Oct23.xlsx")
        expr_file = os.path.join(DATA_DIR, "Expression_Data_subset.csv")
        
        df_resp = pd.read_excel(response_file)
        df_resp = df_resp.rename(columns={'CELL_LINE_NAME': 'Cell_Line', 'DRUG_NAME': 'Drug', 'LN_IC50': 'IC50'})
        
        df_expr = pd.read_csv(expr_file, index_col=0) 
        return df_resp, df_expr
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def process_biomarkers(df_resp, df_expr, drug_name, test_size=0.2):
    """
    Merges data, splits BEFORE stats to prevent leakage, 
    calculates FDR, and returns train/test sets.
    """
    drug_data = df_resp[df_resp['Drug'] == drug_name].copy()
    if drug_data.empty: return None, None, None
    
    expr_t = df_expr.T
    merged = pd.merge(drug_data, expr_t, left_on='Cell_Line', right_index=True, how='inner')
    
    if len(merged) < 10:
        return None, None, None

    # 1. SPLIT FIRST (Crucial for preventing data leakage)
    train_df, test_df = train_test_split(merged, test_size=test_size, random_state=42)
    
    # 2. Calculate stats ONLY on training data
    gene_cols = expr_t.columns
    ic50_train = train_df['IC50']
    
    results = []
    for gene in gene_cols:
        clean_train = train_df[[gene, 'IC50']].dropna()
        # Require at least 5 samples and non-zero variance
        if len(clean_train) > 5 and clean_train[gene].std() > 0:
            corr, p = stats.pearsonr(clean_train[gene], clean_train['IC50'])
            results.append({'Gene': gene, 'Correlation': corr, 'P_Value': p})
            
    results_df = pd.DataFrame(results)
    if results_df.empty: return train_df, test_df, None
        
    # 3. FDR Correction
    p_vals = results_df['P_Value'].values
    reject, p_adj, _, _ = multipletests(p_vals, alpha=0.05, method='fdr_bh')
    results_df['P_Value_FDR'] = p_adj
    results_df['-log10_P_Raw'] = -np.log10(results_df['P_Value'] + 1e-300)
    
    # 4. Define Significance using FDR (Fixes P0-3)
    results_df['Significant'] = (results_df['P_Value_FDR'] < 0.05) & (results_df['Correlation'].abs() > 0.2)
    
    # 5. Sort by FDR for ML feature selection (Fixes P0-4)
    results_df = results_df.sort_values('P_Value_FDR')
    
    return train_df, test_df, results_df
