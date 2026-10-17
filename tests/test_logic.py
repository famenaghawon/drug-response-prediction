import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_loader import get_ml_features
import pandas as pd

def test_get_ml_features():
    # Create a dummy dataframe to test the feature extractor
    dummy_df = pd.DataFrame({
        'Gene': ['G1', 'G2', 'G3', 'G4', 'G5', 'G6'],
        'Significant': [True, True, True, True, True, True]
    })
    features = get_ml_features(dummy_df, top_n=3)
    assert len(features) == 3
    assert features == ['G1', 'G2', 'G3']
