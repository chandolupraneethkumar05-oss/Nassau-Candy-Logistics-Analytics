"""
Nassau Candy Logistics Analytics - Visualization Pipeline
Generates high-resolution executive charts using a natural corporate color palette.
Reflects standardized Route Efficiency Index (REI) and realistic supply chain metrics.
"""

import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_clean_data
from src.config import COLORS

# Create charts directory
os.makedirs("charts", exist_ok=True)

# Set clean matplotlib corporate style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#F1F5F9"

# Load clean dataset and route summary
df = load_clean_data("data/cleaned_dataset.csv")
route_summary = pd.read_csv("output/route_summary.csv")
reliable_routes = route_summary[route_summary["Is_Reliable"]].copy()

# -------------------------------------------------------------
# 1. Ship Mode Distribution
# -------------------------------------------------------------
plt.figure(figsize=(8, 5))
ship_counts = df["Ship Mode"].value_counts()
colors = [COLORS["primary"], COLORS["primary_light"], COLORS["accent_warm"], COLORS["secondary"]]
bars = plt.bar(ship_counts.index, ship_counts.values, color=colors, width=0.55, edgecolor="#1E293B", linewidth=0.5)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 100, f"{int(yval):,}", ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E293B")

plt.title("Shipment Volume by Service Tier", fontsize=14, fontweight="bold", pad=15, color="#0F172A")
plt.xlabel("Shipping Mode", fontsize=11, fontweight="bold", labelpad=8, color="#334155")
plt.ylabel("Number of Orders", fontsize=11, fontweight="bold", labelpad=8, color="#334155")
plt.ylim(0, max(ship_counts.values) * 1.12)
plt.tight_layout()
plt.savefig("charts/ship_mode_distribution.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# 2. Region-wise Average Lead Time & Transit Breakdown
# -------------------------------------------------------------
region_metrics = df.groupby("Region")[["Fulfillment Days", "Transit Days"]].mean().loc[["Pacific", "Atlantic", "Interior", "Gulf"]]

plt.figure(figsize=(9, 5))
x = range(len(region_metrics))
width = 0.35
plt.bar([p - width/2 for p in x], region_metrics["Fulfillment Days"], width=width, label="Fulfillment Delay (Days)", color=COLORS["primary"], edgecolor="white")
plt.bar([p + width/2 for p in x], region_metrics["Transit Days"], width=width, label="Transit Duration (Days)", color=COLORS["accent_warm"], edgecolor="white")

plt.title("Regional Lead Time Breakdown (Fulfillment vs. Transit)", fontsize=14, fontweight="bold", pad=15, color="#0F172A")
plt.xlabel("Region", fontsize=11, fontweight="bold", labelpad=8, color="#334155")
plt.ylabel("Average Days", fontsize=11, fontweight="bold", labelpad=8, color="#334155")
plt.xticks(x, region_metrics.index)
plt.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0")
plt.tight_layout()
plt.savefig("charts/region_leadtime.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# 3. Top 10 Most Efficient Corridors (REI)
# -------------------------------------------------------------
top10 = reliable_routes.nlargest(10, "Efficiency Score").sort_values("Efficiency Score", ascending=True)

plt.figure(figsize=(10, 6))
bars = plt.barh(top10["Route"], top10["Efficiency Score"], color=COLORS["accent_green"], height=0.6, edgecolor="#14532D", linewidth=0.5)

for bar in bars:
    val = bar.get_width()
    plt.text(val + 0.8, bar.get_y() + bar.get_height()/2.0, f"{val:.1f}", ha="left", va="center", fontsize=9, fontweight="bold", color="#14532D")

plt.title("Top 10 Most Efficient Shipping Corridors (REI Score)", fontsize=14, fontweight="bold", pad=15, color="#0F172A")
plt.xlabel("Route Efficiency Index (0-100)", fontsize=11, fontweight="bold", labelpad=8, color="#334155")
plt.xlim(0, max(top10["Efficiency Score"]) * 1.15)
plt.tight_layout()
plt.savefig("charts/top10_routes.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# 4. Bottom 10 Routes Requiring Attention
# -------------------------------------------------------------
bottom10 = reliable_routes.nsmallest(10, "Efficiency Score").sort_values("Efficiency Score", ascending=False)

plt.figure(figsize=(10, 6))
bars = plt.barh(bottom10["Route"], bottom10["Efficiency Score"], color=COLORS["accent_red"], height=0.6, edgecolor="#7F1D1D", linewidth=0.5)

for bar in bars:
    val = bar.get_width()
    plt.text(val + 0.8, bar.get_y() + bar.get_height()/2.0, f"{val:.1f}", ha="left", va="center", fontsize=9, fontweight="bold", color="#7F1D1D")

plt.title("Bottom 10 Corridors Requiring Attention (Low REI Score)", fontsize=14, fontweight="bold", pad=15, color="#0F172A")
plt.xlabel("Route Efficiency Index (0-100)", fontsize=11, fontweight="bold", labelpad=8, color="#334155")
plt.xlim(0, max(bottom10["Efficiency Score"]) * 1.25)
plt.tight_layout()
plt.savefig("charts/bottom10_routes.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# 5. Sales & Profitability by Region
# -------------------------------------------------------------
reg_fin = df.groupby("Region")[["Sales", "Gross Profit"]].sum().sort_values("Sales", ascending=True)

plt.figure(figsize=(9, 5))
x = range(len(reg_fin))
width = 0.35
plt.bar([p - width/2 for p in x], reg_fin["Sales"] / 1000, width=width, label="Sales ($K)", color=COLORS["primary"], edgecolor="white")
plt.bar([p + width/2 for p in x], reg_fin["Gross Profit"] / 1000, width=width, label="Gross Profit ($K)", color=COLORS["accent_green"], edgecolor="white")

plt.title("Commercial Performance by Region (Sales vs. Gross Profit)", fontsize=14, fontweight="bold", pad=15, color="#0F172A")
plt.xlabel("Region", fontsize=11, fontweight="bold", labelpad=8, color="#334155")
plt.ylabel("Amount ($ in Thousands)", fontsize=11, fontweight="bold", labelpad=8, color="#334155")
plt.xticks(x, reg_fin.index)
plt.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0")
plt.tight_layout()
plt.savefig("charts/sales_by_region.png", dpi=200)
plt.close()

print("\nAll 5 executive charts generated successfully in natural corporate palette!")