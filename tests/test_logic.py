import pytest
import pandas as pd
import numpy as np
import sys
import os

# This line tells Python to look in the root folder for the 'src' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import process_biomarkers
from src.model import train_drug_model

def test_pipeline_end_to_end():
    # Create dummy data
    np.random.seed(42)
    genes = [f"Gene_{i}" for i in range(10)]
    cell_lines = [f"Cell_{i}" for i in range(20)]
    
    # Dummy expression
    expr_data = np.random.rand(10, 20)
    df_expr = pd.DataFrame(expr_data, index=genes, columns=cell_lines)
    
    # Dummy response
    df_resp = pd.DataFrame({
        'Cell_Line': cell_lines,
        'Drug': ['Erlotinib'] * 20,
        'IC50': np.random.rand(20)
    })
    
    train_df, test_df, results_df = process_biomarkers(df_resp, df_expr, 'Erlotinib')
    
    assert train_df is not None
    assert len(train_df) == 16
    assert len(test_df) == 4
    assert results_df is not None
    
    top_genes = results_df['Gene'].head(5).tolist()
    model, metrics, pred_df = train_drug_model(train_df, test_df, top_genes)
    
    assert 'test_r2' in metrics
    assert len(pred_df) == 4
