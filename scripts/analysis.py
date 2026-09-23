"""
Nassau Candy Logistics Analytics - Route & Performance Analysis Script
Processes the cleaned shipment dataset, computes the standardized Route Efficiency Index (REI),
identifies high-performing and bottleneck corridors, and exports summary reports.
"""

import os
import sys
import pandas as pd

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_clean_data
from src.logistics import calculate_route_summary


def run_logistics_analysis():
    print("=" * 60)
    print("Nassau Candy Distributor - Route Efficiency & Performance Analysis")
    print("=" * 60)

    # 1. Load Cleaned Dataset
    df = load_clean_data("data/cleaned_dataset.csv")
    print(f"Loaded cleaned dataset with {len(df):,} records.")

    # 2. Compute Route Summary using standardized REI
    route_summary = calculate_route_summary(df, min_shipments=5)
    print(f"Aggregated {len(route_summary):,} distinct factory-to-destination routes.")

    # 3. Filter for statistically reliable routes (N >= 5 shipments)
    reliable_routes = route_summary[route_summary["Is_Reliable"]].copy()
    print(f"Statistically reliable routes (N >= 5 shipments): {len(reliable_routes):,}")

    # 4. Top 10 and Bottom 10 Routes by Route Efficiency Index
    top10 = reliable_routes.sort_values("Efficiency Score", ascending=False).head(10)
    bottom10 = reliable_routes.sort_values("Efficiency Score", ascending=True).head(10)

    # 5. Export results
    os.makedirs("output", exist_ok=True)
    route_summary.to_csv("output/route_summary.csv", index=False)
    top10.to_csv("output/top10_routes.csv", index=False)
    bottom10.to_csv("output/bottom10_routes.csv", index=False)

    print("\n--- Top 5 Most Efficient Routes (REI Score) ---")
    print(top10[["Route", "Shipments", "Avg_Distance_Miles", "Avg_Total_Lead_Time", "Profit_Margin_Pct", "Efficiency Score"]].head(5).to_string(index=False))

    print("\n--- Bottom 5 Routes Requiring Attention ---")
    print(bottom10[["Route", "Shipments", "Avg_Distance_Miles", "Avg_Total_Lead_Time", "Profit_Margin_Pct", "Efficiency Score"]].head(5).to_string(index=False))

    print("\nReports successfully saved in output/ directory:")
    print(" - output/route_summary.csv")
    print(" - output/top10_routes.csv")
    print(" - output/bottom10_routes.csv")
    print("=" * 60)


if __name__ == "__main__":
    run_logistics_analysis()
