import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
import os
from sklearn.model_selection import train_test_split
import streamlit as st
from datasets import load_dataset

DATA_DIR = "data/raw"

# ============================================================
# 🌐 REMOTE DATA FETCHING (Hugging Face)
# ============================================================
@st.cache_data(show_spinner="⚡ Streaming gene expression data via HF Xet...")
def fetch_expression_data():
    try:
        # This uses HF's optimized engine to download the file instantly
        dataset = load_dataset("famenaghawon/drug-response-data", split="train")
        df_expr = dataset.to_pandas()
        
        # Ensure the first column is set as the index (just like pd.read_csv(index_col=0))
        if df_expr.columns[0] not in ['Gene', 'Cell_Line']: 
            df_expr.set_index(df_expr.columns[0], inplace=True)
            
        return df_expr
    except Exception as e:
        st.error(f"Failed to stream data from Hugging Face: {e}")
        return None

# ============================================================
# 📊 MAIN DATA LOADER
# ============================================================
def load_gdsc_data():
    """Loads real GDSC data and standardizes column names."""
    try:
        response_file = os.path.join(DATA_DIR, "GDSC2_fitted_dose_response_27Oct23.xlsx")
        expr_file = os.path.join(DATA_DIR, "Expression_Data_subset.csv")
       
        
        if os.path.exists(response_file):
            df_resp = pd.read_excel(response_file)
        else:
            # Fallback URL for response data (replace with actual URL if needed)
            st.warning(f"Local response file not found at {response_file}. Attempting fallback...")
            return None, None
            
        df_resp = df_resp.rename(columns={'CELL_LINE_NAME': 'Cell_Line', 'DRUG_NAME': 'Drug', 'LN_IC50': 'IC50'})
       
        # 2. Load Expression Data (Massive 230MB file)
        if os.path.exists(expr_file):
            # If running locally and file exists, use local (faster)
            df_expr = pd.read_csv(expr_file, index_col=0)
        else:
            # If on Streamlit Cloud (or file missing), stream from Hugging Face
            df_expr = fetch_expression_data()
            
        if df_expr is None:
            return None, None

        return df_resp, df_expr
    except Exception as e:
        st.error(f"Error loading data pipeline: {e}")
        return None, None


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

    # 1. SPLIT FIRST (Crucial for preventing data leakage)
    train_df, test_df = train_test_split(merged, test_size=test_size, random_state=42)
   
    # 2. Calculate stats ONLY on training data
    gene_cols = expr_t.columns
    # Optional: filter to ensure we only test valid gene columns
    gene_cols = [col for col in gene_cols if col in train_df.columns]
    
    results = []
    
    # Using a faster loop for 41k genes
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
   
    # 4. Define Significance using FDR
    results_df['Significant'] = (results_df['P_Value_FDR'] < 0.05) & (results_df['Correlation'].abs() > 0.2)
   
    # 5. Sort by FDR for ML feature selection
    results_df = results_df.sort_values('P_Value_FDR')
   
    return train_df, test_df, results_df
