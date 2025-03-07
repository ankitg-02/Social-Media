import unittest
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Low-Level Design: Define modular functions
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def preprocess_data(df, target_column):
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    return r2_score(y_test, y_pred)

# Unit Tests
class TestMLPipeline(unittest.TestCase):
    def setUp(self):
        data = {
            'feature1': np.random.rand(100),
            'feature2': np.random.rand(100),
            'target': np.random.rand(100)
        }
        self.df = pd.DataFrame(data)
    
    def test_load_data(self):
        df = load_data('Time-Wasters on Social Media.csv')  # Replace with actual test file
        self.assertIsInstance(df, pd.DataFrame)
    
    def test_preprocess_data(self):
        X_train, X_test, y_train, y_test = preprocess_data(self.df, 'target')
        self.assertEqual(len(X_train) + len(X_test), 100)
    
    def test_train_model(self):
        X_train, X_test, y_train, y_test = preprocess_data(self.df, 'target')
        model = train_model(X_train, y_train)
        self.assertIsInstance(model, LinearRegression)
    
    def test_evaluate_model(self):
        X_train, X_test, y_train, y_test = preprocess_data(self.df, 'target')
        model = train_model(X_train, y_train)
        score = evaluate_model(model, X_test, y_test)
        self.assertIsInstance(score, float)

if __name__ == "__main__":
    unittest.main()
