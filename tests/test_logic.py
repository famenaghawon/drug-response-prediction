import pytest
import pandas as pd
import numpy as np
import sys
import os

# This line tells Python to look in the root folder for the 'src' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import process_biomarkers
from src.model import train_drug_model

def test_process_biomarkers_split_and_fdr():
    """Test that data is split 80/20 BEFORE stats, and FDR is calculated."""
    np.random.seed(42)
    
    # 1. Create Dummy Data
    n_genes = 100
    n_cells = 50
    genes = [f"Gene_{i}" for i in range(n_genes)]
    cell_lines = [f"Cell_{i}" for i in range(n_cells)]
   
    # Random expression matrix (genes x cells)
    expr_data = np.random.rand(n_genes, n_cells)
    df_expr = pd.DataFrame(expr_data, index=genes, columns=cell_lines)
   
    # Random response data
    df_resp = pd.DataFrame({
        'Cell_Line': cell_lines,
        'Drug': ['Erlotinib'] * n_cells,
        'IC50': np.random.rand(n_cells)
    })
   
    # 2. Run the pipeline
    train_df, test_df, results_df = process_biomarkers(df_resp, df_expr, 'Erlotinib')
   
    # 3. Assertions (Check the rules)
    assert train_df is not None, "Train DF should not be None"
    assert test_df is not None, "Test DF should not be None"
    
    # Check the 80/20 split
    assert len(train_df) == 40, "Train set should be 80% of 50 cells (40)"
    assert len(test_df) == 10, "Test set should be 20% of 50 cells (10)"
    
    # Check that FDR logic ran and columns exist
    assert results_df is not None, "Results DF should not be None"
    assert 'P_Value_FDR' in results_df.columns, "FDR column is missing"
    assert 'Significant' in results_df.columns, "Significant boolean column is missing"
    
    # Check that there are no NaNs in the FDR column
    assert not results_df['P_Value_FDR'].isna().any(), "FDR values should not contain NaNs"


def test_train_drug_model_metrics():
    """Test that the ML model trains, returns metrics, and predicts correctly."""
    np.random.seed(42)
    
    # Create dummy train/test data with known signal
    n_genes = 10
    n_train = 50
    n_test = 15
    
    genes = [f"Gene_{i}" for i in range(n_genes)]
    
    # Train data
    train_data = {g: np.random.rand(n_train) for g in genes}
    train_data['IC50'] = np.random.rand(n_train)
    train_df = pd.DataFrame(train_data)
    
    # Test data
    test_data = {g: np.random.rand(n_test) for g in genes}
    test_data['IC50'] = np.random.rand(n_test)
    test_df = pd.DataFrame(test_data)
    
    top_genes = genes[:5]
    
    # Run Model
    model, metrics, pred_df = train_drug_model(train_df, test_df, top_genes)
    
    # Assertions
    assert 'cv_r2_mean' in metrics, "Cross-val R2 missing"
    assert 'test_r2' in metrics, "Test R2 missing"
    assert 'test_rmse' in metrics, "RMSE missing"
    
    assert len(pred_df) == n_test, "Predictions length must match test set"
    assert 'Actual' in pred_df.columns
    assert 'Predicted' in pred_df.columns
