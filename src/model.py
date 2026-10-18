from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np

def train_drug_model(train_df, test_df, top_genes):
    """
    Trains RF with train-only imputation and 5-Fold CV.
    Evaluates on completely unseen test set.
    """
    # Train-only imputation
    train_medians = train_df[top_genes].median()
    X_train = train_df[top_genes].fillna(train_medians).values
    y_train = train_df['IC50'].values
    
    X_test = test_df[top_genes].fillna(train_medians).values
    y_test = test_df['IC50'].values
    
    rf = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
    
    # Cross-Validation on TRAIN only
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(rf, X_train, y_train, cv=kf, scoring='r2')
    
    # Fit on Train
    rf.fit(X_train, y_train)
    
    # Evaluate on unseen Test
    y_pred = rf.predict(X_test)
    test_r2 = r2_score(y_test, y_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    metrics = {
        'cv_r2_mean': cv_scores.mean(),
        'test_r2': test_r2,
        'test_rmse': test_rmse
    }
    
    pred_df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    
    return rf, metrics, pred_df
