"""Quick verification of cleaned dataset columns."""
import pandas as pd

df = pd.read_csv("data/cleaned_dataset.csv")

print(f"\nDataset Dimensions: {df.shape[0]:,} rows x {df.shape[1]} columns\n")
print("Cleaned Columns:")
for i, col in enumerate(df.columns, 1):
    print(f" {i:2d}. {col} (type: {df[col].dtype})")