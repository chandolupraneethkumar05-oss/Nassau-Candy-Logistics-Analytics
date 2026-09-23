"""
Nassau Candy Logistics Analytics - Genuine Machine Learning Engine
Implements scikit-learn models for:
1. Total Lead Time Regression (Random Forest Regressor)
2. On-Time Delivery Risk Classification (Gradient Boosting / Random Forest Classifier)
Provides interactive 'What-If' prediction capabilities for supply chain planners.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score


class LogisticsMLPredictor:
    def __init__(self):
        self.regression_pipeline = None
        self.classification_pipeline = None
        self.metrics = {}
        self.feature_names = []
        self.is_trained = False

    def train(self, df: pd.DataFrame):
        """
        Trains the regression and classification models using shipment data.
        """
        required_cols = ["Factory", "State/Province", "Ship Mode", "Units",
                         "Distance Miles", "Total Lead Time", "On Time"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required ML column: {col}")

        X = df[["Factory", "State/Province", "Ship Mode", "Units", "Distance Miles"]].copy()
        y_reg = df["Total Lead Time"]
        y_clf = df["On Time"].astype(int)

        categorical_features = ["Factory", "State/Province", "Ship Mode"]
        numerical_features = ["Units", "Distance Miles"]

        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
                ("num", "passthrough", numerical_features)
            ]
        )

        # 1. Regressor for Lead Time Days
        reg_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, max_depth=12)
        self.regression_pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", reg_model)
        ])

        # 2. Classifier for On-Time SLA Delivery
        clf_model = GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=4)
        self.classification_pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", clf_model)
        ])

        # Split and train
        X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(
            X, y_reg, y_clf, test_size=0.2, random_state=42
        )

        self.regression_pipeline.fit(X_train, y_reg_train)
        y_reg_pred = self.regression_pipeline.predict(X_test)
        mae = mean_absolute_error(y_reg_test, y_reg_pred)
        r2 = r2_score(y_reg_test, y_reg_pred)

        self.classification_pipeline.fit(X_train, y_clf_train)
        y_clf_pred = self.classification_pipeline.predict(X_test)
        acc = accuracy_score(y_clf_test, y_clf_pred)

        self.metrics = {
            "mae_days": round(mae, 2),
            "r2_score": round(r2, 3),
            "accuracy": round(acc * 100, 1),
            "sample_size": len(X)
        }
        self.is_trained = True
        return self.metrics

    def predict(self, factory: str, state: str, ship_mode: str, units: int, distance_miles: float) -> dict:
        """
        Runs real-time inference for a hypothetical or new shipment.
        """
        if not self.is_trained:
            raise RuntimeError("Model has not been trained yet.")

        input_df = pd.DataFrame([{
            "Factory": factory,
            "State/Province": state,
            "Ship Mode": ship_mode,
            "Units": units,
            "Distance Miles": distance_miles
        }])

        pred_lead_time = self.regression_pipeline.predict(input_df)[0]
        on_time_prob = self.classification_pipeline.predict_proba(input_df)[0][1]

        return {
            "predicted_lead_time_days": round(float(pred_lead_time), 1),
            "on_time_probability": round(float(on_time_prob) * 100, 1),
            "estimated_delivery_risk": "Low" if on_time_prob >= 0.85 else ("Medium" if on_time_prob >= 0.65 else "High")
        }


# Global singleton cache for trained model
_predictor_instance = None


def get_trained_predictor(df: pd.DataFrame) -> LogisticsMLPredictor:
    """Returns a trained singleton instance of LogisticsMLPredictor."""
    global _predictor_instance
    if _predictor_instance is None or not _predictor_instance.is_trained:
        predictor = LogisticsMLPredictor()
        predictor.train(df)
        _predictor_instance = predictor
    return _predictor_instance
