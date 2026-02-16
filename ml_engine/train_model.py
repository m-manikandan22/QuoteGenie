
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import pickle
import os

# Define paths
DATA_PATH = "../data/historical_quotes.csv"
MODEL_PATH = "models/win_prob_model.json"

def load_data():
    if not os.path.exists(DATA_PATH):
        print(f"Data file not found at {DATA_PATH}. Creating dummy data.")
        # Create dummy data for demonstration
        data = pd.DataFrame({
            'weight': np.random.uniform(1, 1000, 100),
            'distance': np.random.uniform(10, 2000, 100),
            'price': np.random.uniform(50, 5000, 100),
            'competitor_rate': np.random.uniform(40, 4800, 100),
            'win': np.random.choice([0, 1], 100)
        })
        return data
    return pd.read_csv(DATA_PATH)

def train_win_probability_model():
    print("Loading data...")
    df = load_data()
    
    X = df[['weight', 'distance', 'price', 'competitor_rate']]
    y = df['win']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    
    print(f"Model Accuracy: {accuracy:.2f}")
    print(f"Model AUC: {auc:.2f}")
    
    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    model.save_model(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_win_probability_model()
