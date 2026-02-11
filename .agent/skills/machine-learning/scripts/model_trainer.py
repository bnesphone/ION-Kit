#!/usr/bin/env python3
"""
Machine Learning Model Trainer
Trains and evaluates ML models on CSV data

Usage: python model_trainer.py data.csv [--target column_name] [--model rf|xgb|lr]
"""
import sys
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import json

def load_and_prepare_data(filepath, target_col=None):
    """Load CSV and prepare for training"""
    df = pd.read_csv(filepath)
    
    # Auto-detect target column (last column if not specified)
    if target_col is None:
        target_col = df.columns[-1]
    
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in data")
    
    # Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Handle categorical features (simple one-hot encoding)
    categorical_cols = X.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    
    # Handle missing values
    X = X.fillna(X.median())
    
    return X, y, target_col

def train_model(X, y, model_type='rf'):
    """Train and evaluate model"""
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Select and train model
    if model_type == 'rf':
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
    elif model_type == 'xgb':
        try:
            from xgboost import XGBClassifier
            model = XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        except ImportError:
            print("XGBoost not installed, falling back to Random Forest")
            model = RandomForestClassifier(n_estimators=100, random_state=42)
    elif model_type == 'lr':
        model = LogisticRegression(max_iter=1000, random_state=42)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Train
    print(f"\n[*] Training {model_type.upper()} model...")
    model.fit(X_train_scaled, y_train)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
    print(f"[*] Cross-validation score: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
    
    # Evaluate on test set
    y_pred = model.predict(X_test_scaled)
    test_score = model.score(X_test_scaled, y_test)
    
    print(f"\n[*] Test accuracy: {test_score:.3f}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance (if available)
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_names = X.columns
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Important Features:")
        print(importance_df.head(10).to_string(index=False))
    
    return model, scaler, {
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'test_accuracy': test_score,
        'model_type': model_type
    }

def save_model(model, scaler, metrics, prefix='model'):
    """Save model, scaler, and metrics"""
    model_path = f'{prefix}.pkl'
    scaler_path = f'{prefix}_scaler.pkl'
    metrics_path = f'{prefix}_metrics.json'
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n[SUCCESS] Model saved:")
    print(f"  - Model: {model_path}")
    print(f"  - Scaler: {scaler_path}")
    print(f"  - Metrics: {metrics_path}")

def main():
    parser = argparse.ArgumentParser(description='Train ML model on CSV data')
    parser.add_argument('data', help='Path to CSV file')
    parser.add_argument('--target', help='Target column name (default: last column)')
    parser.add_argument('--model', choices=['rf', 'xgb', 'lr'], default='rf',
                       help='Model type: rf=RandomForest, xgb=XGBoost, lr=LogisticRegression')
    parser.add_argument('--output', default='model', help='Output prefix for saved files')
    
    args = parser.parse_args()
    
    try:
        # Load data
        print(f"[*] Loading data from {args.data}...")
        X, y, target_col = load_and_prepare_data(args.data, args.target)
        print(f"[*] Data shape: {X.shape[0]} rows, {X.shape[1]} features")
        print(f"[*] Target column: {target_col}")
        print(f"[*] Class distribution:\n{y.value_counts()}\n")
        
        # Train model
        model, scaler, metrics = train_model(X, y, args.model)
        
        # Save
        save_model(model, scaler, metrics, args.output)
        
        print("\n[*] Model ready for predictions!")
        print(f"    Load with: joblib.load('{args.output}.pkl')")
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
