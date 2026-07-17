import os
import pandas as pd

# ======================================================
# LOAD DATASET
# ======================================================

df = pd.read_csv("data/Nassau Candy Distributor.csv")

# ======================================================
# DATE CONVERSION
# ======================================================

df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")

# ======================================================
# CREATE LEAD TIME
# ======================================================

df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

# ======================================================
# PRODUCT -> FACTORY
# ======================================================

factory_map = {

"Wonka Bar - Nutty Crunch Surprise":"Lot's O' Nuts",
"Wonka Bar - Fudge Mallows":"Lot's O' Nuts",
"Wonka Bar -Scrumdiddlyumptious":"Lot's O' Nuts",
"Wonka Bar - Milk Chocolate":"Wicked Choccy's",
"Wonka Bar - Triple Dazzle Caramel":"Wicked Choccy's",
"Laffy Taffy":"Sugar Shack",
"SweeTARTS":"Sugar Shack",
"Nerds":"Sugar Shack",
"Fun Dip":"Sugar Shack",
"Fizzy Lifting Drinks":"Sugar Shack",
"Everlasting Gobstopper":"Secret Factory",
"Hair Toffee":"The Other Factory",
"Lickable Wallpaper":"Secret Factory",
"Wonka Gum":"Secret Factory",
"Kazookles":"The Other Factory"

}

df["Factory"] = df["Product Name"].map(factory_map)

# ======================================================
# CREATE ROUTE
# ======================================================

df["Route"] = df["Factory"] + " → " + df["State/Province"]

# ======================================================
# ROUTE SUMMARY
# ======================================================

route_summary = (

    df.groupby("Route")
      .agg(
          Total_Shipments=("Order ID", "count"),
          Average_Lead_Time=("Lead Time", "mean"),
          Lead_Time_STD=("Lead Time", "std"),
          Total_Sales=("Sales", "sum"),
          Total_Gross_Profit=("Gross Profit", "sum")
      )
      .reset_index()

)

# ======================================================
# ROUTE EFFICIENCY SCORE
# ======================================================

max_lead = route_summary["Average_Lead_Time"].max()

route_summary["Efficiency Score"] = (
    100 -
    (
        route_summary["Average_Lead_Time"] / max_lead
    ) * 100
)

# ======================================================
# TOP & BOTTOM ROUTES
# ======================================================

top10 = route_summary.sort_values(
    "Efficiency Score",
    ascending=False
).head(10)

bottom10 = route_summary.sort_values(
    "Efficiency Score"
).head(10)

# ======================================================
# SAVE FILES
# ======================================================

os.makedirs("output", exist_ok=True)

route_summary.to_csv(
    "output/route_summary.csv",
    index=False
)

top10.to_csv(
    "output/top10_routes.csv",
    index=False
)

bottom10.to_csv(
    "output/bottom10_routes.csv",
    index=False
)

# ======================================================
# PRINT RESULTS
# ======================================================

print("\n==============================")
print("Total Routes")
print("==============================")
print(route_summary.shape[0])

print("\n==============================")
print("Top 10 Routes")
print("==============================")
print(top10)

print("\n==============================")
print("Bottom 10 Routes")
print("==============================")
print(bottom10)

print("\nFiles Created Successfully")
print("route_summary.csv")
print("top10_routes.csv")
print("bottom10_routes.csv")
