import pandas as pd
import matplotlib.pyplot as plt
import os

# Load processed files
df = pd.read_csv("data/cleaned_dataset.csv")
route_summary = pd.read_csv("output/route_summary.csv")

os.makedirs("charts", exist_ok=True)
import os
import matplotlib.pyplot as plt

# Create charts folder
os.makedirs("charts", exist_ok=True)

# -------------------------------
# 1. Ship Mode Distribution
# -------------------------------
plt.figure(figsize=(8,5))
df["Ship Mode"].value_counts().plot(kind="bar")
plt.title("Orders by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("charts/ship_mode_distribution.png")
plt.close()

# -------------------------------
# 2. Region-wise Average Lead Time
# -------------------------------
region_avg = df.groupby("Region")["Lead Time"].mean().sort_values()

plt.figure(figsize=(10,5))
region_avg.plot(kind="bar")
plt.title("Average Lead Time by Region")
plt.xlabel("Region")
plt.ylabel("Lead Time (Days)")
plt.tight_layout()
plt.savefig("charts/region_leadtime.png")
plt.close()

# -------------------------------
# 3. Top 10 Efficient Routes
# -------------------------------
top10 = route_summary.nlargest(10, "Efficiency Score")

plt.figure(figsize=(12,6))
plt.barh(top10["Route"], top10["Efficiency Score"])
plt.title("Top 10 Most Efficient Routes")
plt.xlabel("Efficiency Score")
plt.tight_layout()
plt.savefig("charts/top10_routes.png")
plt.close()

# -------------------------------
# 4. Bottom 10 Efficient Routes
# -------------------------------
bottom10 = route_summary.nsmallest(10, "Efficiency Score")

plt.figure(figsize=(12,6))
plt.barh(bottom10["Route"], bottom10["Efficiency Score"])
plt.title("Bottom 10 Least Efficient Routes")
plt.xlabel("Efficiency Score")
plt.tight_layout()
plt.savefig("charts/bottom10_routes.png")
plt.close()

# -------------------------------
# 5. Sales by Region
# -------------------------------
sales_region = df.groupby("Region")["Sales"].sum().sort_values()

plt.figure(figsize=(10,5))
sales_region.plot(kind="bar")
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("charts/sales_by_region.png")
plt.close()

print("\nCharts Generated Successfully!")
print("-----------------------------")
print("ship_mode_distribution.png")
print("region_leadtime.png")
print("top10_routes.png")
print("bottom10_routes.png")
print("sales_by_region.png")