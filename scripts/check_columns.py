import pandas as pd

df = pd.read_csv("data/cleaned_dataset.csv")

print("\nDataset Columns:\n")
for col in df.columns:
    print(col)