"""
Nassau Candy Logistics Analytics - Centralized Data Loader
Provides cached, validated data loading for all Streamlit pages and analysis scripts.
"""

import os
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_clean_data(file_path: str = "data/cleaned_dataset.csv") -> pd.DataFrame:
    """
    Loads and caches the cleaned Nassau Candy shipment dataset.
    Ensures datetime formatting, route keys, and correct numeric types.
    """
    if not os.path.exists(file_path):
        # Fallback if run from a subdirectory
        file_path = os.path.join(os.path.dirname(__file__), "..", file_path)

    df = pd.read_csv(file_path)

    # Convert dates to datetime
    date_cols = ["Order Date", "Ship Date", "Delivery Date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # Ensure Route column is standardized
    if "Route" not in df.columns and "Factory" in df.columns and "State/Province" in df.columns:
        df["Route"] = df["Factory"] + " -> " + df["State/Province"]

    # Ensure Boolean types
    if "On Time" in df.columns:
        df["On Time"] = df["On Time"].astype(bool)

    return df
