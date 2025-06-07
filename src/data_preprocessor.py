import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.datasets import fetch_openml
from imblearn.over_sampling import SMOTE
import streamlit as st
from pathlib import Path


class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []

    def load_cleveland_dataset(self):
        """Load the Cleveland Heart Disease dataset from a relative path."""
        try:
            # Use current working directory (Jupyter or production)
            base_path = Path.cwd()

            # Try to locate dataset.csv in current dir or 'src/'
            if (base_path / 'dataset.csv').exists():
                dataset_path = base_path / 'dataset.csv'
            elif (base_path / 'src' / 'dataset.csv').exists():
                dataset_path = base_path / 'src' / 'dataset.csv'
            else:
                raise FileNotFoundError(
                    "dataset.csv not found in either current directory or 'src/' folder."
                )

            df = pd.read_csv(dataset_path)

            if df.empty:
                raise ValueError("Dataset is empty.")

        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            df = pd.DataFrame()  # Empty DataFrame fallback

        return df

    def preprocess_data(self, df):
        """Preprocess the heart disease dataset"""
        X = df.drop('target', axis=1)
        y = df['target']

        self.feature_names = X.columns.tolist()
        X = X.fillna(X.median())

        categorical_features = X.select_dtypes(include=['object']).columns
        for feature in categorical_features:
            le = LabelEncoder()
            X[feature] = le.fit_transform(X[feature].astype(str))
            self.label_encoders[feature] = le

        X = X.values.astype(np.float32)
        y = y.values.astype(np.int32)

        return X, y

    def apply_smote(self, X, y):
        """Apply SMOTE for handling class imbalance"""
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X, y)
        return X_resampled, y_resampled

    def scale_features(self, X_train, X_test=None):
        """Scale features using StandardScaler"""
        X_train_scaled = self.scaler.fit_transform(X_train)

        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled

        return X_train_scaled

    def load_and_preprocess_data(self, test_size=0.2, apply_smote=True):
        """Complete data loading and preprocessing pipeline"""
        df = self.load_cleveland_dataset()
        if df.empty:
            st.warning("Dataset is empty or failed to load. Aborting pipeline.")
            return None, None, None, None

        X, y = self.preprocess_data(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        if apply_smote:
            X_train, y_train = self.apply_smote(X_train, y_train)

        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)

        return X_train_scaled, X_test_scaled, y_train, y_test

    def prepare_input_for_prediction(self, input_data):
        """Prepare user input for model prediction"""
        input_array = np.array(input_data).reshape(1, -1)
        input_scaled = self.scaler.transform(input_array)
        return input_scaled

    def get_feature_names(self):
        """Get feature names for interpretability"""
        return self.feature_names
