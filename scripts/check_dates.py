"""Quick verification of cleaned dataset dates and lead times."""
import pandas as pd

df = pd.read_csv("data/cleaned_dataset.csv")

print("\n--- Date Summary ---")
print("Order Date Range:", df["Order Date"].min(), "to", df["Order Date"].max())
print("Ship Date Range: ", df["Ship Date"].min(), "to", df["Ship Date"].max())
print("Delivery Date:   ", df["Delivery Date"].min(), "to", df["Delivery Date"].max())

print("\n--- Lead Time Statistics (in Days) ---")
print("Fulfillment Days (Order to Ship):")
print(f"  Min: {df['Fulfillment Days'].min()}, Mean: {df['Fulfillment Days'].mean():.2f}, Max: {df['Fulfillment Days'].max()}")

print("Transit Days (Ship to Delivery):")
print(f"  Min: {df['Transit Days'].min()}, Mean: {df['Transit Days'].mean():.2f}, Max: {df['Transit Days'].max()}")

print("Total Lead Time (Order to Delivery):")
print(f"  Min: {df['Total Lead Time'].min()}, Mean: {df['Total Lead Time'].mean():.2f}, Max: {df['Total Lead Time'].max()}")

print(f"\nOn-Time Delivery Compliance: {(df['On Time'].mean() * 100):.2f}%")