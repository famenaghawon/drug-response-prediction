from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def train_drug_model(X, y):
    """
    Trains Random Forest with K-Fold CV.
    Returns model, metrics.
    """
    # 1. Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. Initialize Model
    rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    
    # 3. Cross-Validation (The "Proper Validation Story")
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(rf, X_train, y_train, cv=kf, scoring='r2')
    
    # 4. Fit final model
    rf.fit(X_train, y_train)
    
    # 5. Evaluate on hold-out test set
    y_pred = rf.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    metrics = {
        'cv_r2_mean': cv_scores.mean(),
        'cv_r2_std': cv_scores.std(),
        'test_r2': r2,
        'test_rmse': rmse
    }
    
    return rf, metrics
