---
name: machine-learning
description: Machine learning model development, training, evaluation, and deployment. Covers supervised/unsupervised learning, deep learning, feature engineering, model selection.
allowed-tools: Read, Write, Bash
---

# Machine Learning Skill

> Expert knowledge in ML algorithms, model training, evaluation, and deployment

## Model Selection Matrix

| Task Type | Algorithm | Best For | Complexity |
|-----------|-----------|----------|------------|
| **Binary Classification** | Logistic Regression | Baseline, interpretability | Low |
| | Random Forest | Tabular data, robust | Medium |
| | XGBoost/LightGBM | Best performance, competitions | Medium |
| | Neural Networks | Images, text, complex patterns | High |
| **Multi-class Classification** | Random Forest | Tabular, multiple classes | Medium |
| | Softmax Regression | Baseline | Low |
| | Deep Learning | Images, NLP | High |
| **Regression** | Linear Regression | Linear relationships | Low |
| | Ridge/Lasso | Regularization needed | Low |
| | Gradient Boosting | Best performance | Medium |
| | Neural Networks | Complex non-linear | High |
| **Clustering** | K-Means | Well-separated groups | Low |
| | DBSCAN | Arbitrary shapes, noise | Medium |
| | Hierarchical | Dendrogram needed | Medium |
| **Dimensionality Reduction** | PCA | Linear relationships | Low |
| | t-SNE | Visualization | Medium |
| | UMAP | Better than t-SNE | Medium |

---

## Training Workflow

### 1. Data Preparation

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Split data (60/20/20)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.4, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
```

### 2. Baseline Model

Always start with a simple baseline:

```python
from sklearn.dummy import DummyClassifier

baseline = DummyClassifier(strategy='most_frequent')
baseline.fit(X_train, y_train)
baseline_score = baseline.score(X_test, y_test)
print(f"Baseline accuracy: {baseline_score:.3f}")
```

### 3. Model Training

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
model.fit(X_train_scaled, y_train)

# Cross-validation
cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
print(f"CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
```

### 4. Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='f1_weighted',
    n_jobs=-1
)
grid_search.fit(X_train_scaled, y_train)

print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")
```

### 5. Model Evaluation

```python
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Predictions
y_pred = model.predict(X_test_scaled)

# Classification report
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d')
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()

# Feature importance
importances = model.feature_importances_
feature_names = X.columns
feature_importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values('importance', ascending=False)
print(feature_importance_df.head(10))
```

---

## Feature Engineering

### Numeric Features

```python
import pandas as pd
import numpy as np

# Missing values
df['col'].fillna(df['col'].median(), inplace=True)

# Outliers (clip to 1st-99th percentile)
lower = df['col'].quantile(0.01)
upper = df['col'].quantile(0.99)
df['col'] = df['col'].clip(lower, upper)

# Create polynomial features
df['col_squared'] = df['col'] ** 2
df['col_log'] = np.log1p(df['col'])

# Binning
df['col_binned'] = pd.cut(df['col'], bins=5, labels=['very_low', 'low', 'med', 'high', 'very_high'])
```

### Categorical Features

```python
# One-hot encoding
df_encoded = pd.get_dummies(df, columns=['category'], prefix='cat')

# Label encoding (for tree-based models)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])

# Target encoding
category_means = df.groupby('category')['target'].mean()
df['category_target_encoded'] = df['category'].map(category_means)
```

### Time Features

```python
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['quarter'] = df['date'].dt.quarter
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
```

---

## Deep Learning

### Simple Neural Network

```python
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    X_train_scaled, y_train,
    validation_data=(X_val_scaled, y_val),
    epochs=50,
    batch_size=32,
    callbacks=[
        keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
    ]
)
```

---

## Model Deployment

### Save Model

```python
import joblib

# Scikit-learn models
joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Load
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
```

### API Endpoint

```python
from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

@app.post("/predict")
async def predict(features: dict):
    # Convert to DataFrame
    df = pd.DataFrame([features])
    
    # Scale
    X_scaled = scaler.transform(df)
    
    # Predict
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0]
    
    return {
        "prediction": int(prediction),
        "probability": float(probability[1])
    }
```

---

## Common Pitfalls

### ❌ Don't

- Train on entire dataset (no test set)
- Use test set for hyperparameter tuning
- Forget to scale features
- Ignore class imbalance
- Use accuracy for imbalanced data
- Overfit to validation set

### ✅ Do

- Always split train/val/test
- Use cross-validation
- Scale features before training
- Handle class imbalance (SMOTE, class weights)
- Use appropriate metrics (F1, AUC for imbalanced)
- Monitor validation metrics

---

## Metrics Guide

### Classification Metrics

| Metric | Use When | Formula |
|--------|----------|---------|
| **Accuracy** | Balanced classes | (TP+TN)/(TP+TN+FP+FN) |
| **Precision** | False positives costly | TP/(TP+FP) |
| **Recall** | False negatives costly | TP/(TP+FN) |
| **F1 Score** | Balance precision/recall | 2*(P*R)/(P+R) |
| **AUC-ROC** | Overall performance | Area under ROC curve |

### Regression Metrics

| Metric | Use When |
|--------|----------|
| **MAE** | Interpretable, robust to outliers |
| **MSE** | Penalize large errors more |
| **RMSE** | Same units as target |
| **R²** | Proportion of variance explained |

---

## Quick Reference

### Model Checklist

- [ ] Data split (train/val/test)
- [ ] Handle missing values
- [ ] Scale features
- [ ] Encode categoricals
- [ ] Train baseline model
- [ ] Train advanced model
- [ ] Cross-validation
- [ ] Hyperparameter tuning
- [ ] Evaluate on test set
- [ ] Check feature importance
- [ ] Save model and scaler
- [ ] Document assumptions
- [ ] Monitor in production

### When to Use What

**Small data (<10k rows):** Linear models, Random Forest
**Large data (>100k rows):** Gradient Boosting, Deep Learning
**Interpretability needed:** Linear models, Decision Trees
**Best performance:** XGBoost, LightGBM, Neural Networks
**Fast inference:** Linear models, small trees
**Images/Text:** Deep Learning (CNNs, Transformers)
