import pandas as pd

df = pd.read_csv("data/cleaned_dataset.csv")

print(df["Order Date"].head(10))
print("\nDatatype:", df["Order Date"].dtype)