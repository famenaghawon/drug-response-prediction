import pandas as pd
import numpy as np
import streamlit as st
import os
from scipy import stats
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import train_test_split

DATA_DIR = "data/raw"

@st.cache_data(show_spinner="⚡ Streaming gene expression data...")
def fetch_expression_data():
    url = "https://huggingface.co/datasets/famenaghawon/drug-response-data/resolve/main/Expression_Data.parquet"
    try:
        return pd.read_parquet(url)
    except Exception as e:
        st.error(f"Failed to stream expression data: {e}")
        return None

@st.cache_data(show_spinner="⚡ Streaming response data...")
def fetch_response_data():
    url = "https://huggingface.co/datasets/famenaghawon/drug-response-data/resolve/main/GDSC2_response.csv"
    try:
        df_resp = pd.read_csv(url)
        df_resp = df_resp.rename(columns={'CELL_LINE_NAME': 'Cell_Line', 'DRUG_NAME': 'Drug', 'LN_IC50': 'IC50'})
        return df_resp
    except Exception as e:
        st.error(f"Failed to stream response data: {e}")
        return None

def load_gdsc_data():
    """Loads real GDSC data directly from Hugging Face."""
    df_resp = fetch_response_data()
    df_expr = fetch_expression_data()
    
    if df_resp is None or df_expr is None:
        return None, None
        
    return df_resp, df_expr

# ============================================================
# 🧬 BIOMARKER PROCESSING
# ============================================================
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

    
    train_df, test_df = train_test_split(merged, test_size=test_size, random_state=42)
   
    
    gene_cols = expr_t.columns
    
    gene_cols = [col for col in gene_cols if col in train_df.columns]
    
    results = []
    
    
    for gene in gene_cols:
        clean_train = train_df[[gene, 'IC50']].dropna()
        # Require at least 5 samples and non-zero variance
        if len(clean_train) > 5 and clean_train[gene].std() > 0:
            corr, p = stats.pearsonr(clean_train[gene], clean_train['IC50'])
            results.append({'Gene': gene, 'Correlation': corr, 'P_Value': p})
           
    results_df = pd.DataFrame(results)
    if results_df.empty: return train_df, test_df, None
       
    
    p_vals = results_df['P_Value'].values
    reject, p_adj, _, _ = multipletests(p_vals, alpha=0.05, method='fdr_bh')
    results_df['P_Value_FDR'] = p_adj
    results_df['-log10_P_Raw'] = -np.log10(results_df['P_Value'] + 1e-300)
   
    
    results_df['Significant'] = (results_df['P_Value_FDR'] < 0.05) & (results_df['Correlation'].abs() > 0.2)
   
    
    results_df = results_df.sort_values('P_Value_FDR')
   
    return train_df, test_df, results_df
