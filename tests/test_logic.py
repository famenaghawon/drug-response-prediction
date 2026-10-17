import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.model import train_drug_model
import numpy as np

def test_model_training():
    # Create fake data for testing logic
    X = np.random.rand(100, 5)
    y = np.random.rand(100)
    
    model, metrics = train_drug_model(X, y)
    
    assert model is not None
    assert metrics['test_r2'] is not None
    assert isinstance(metrics['test_rmse'], float)
    print("Model logic works.")
