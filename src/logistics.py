"""
Nassau Candy Logistics Analytics - Core Logistics & Analytical Engine
Implements Haversine geodesic distance, statistically sound Route Efficiency Index (REI),
SLA performance tracking, and dynamic business recommendations.
"""

import math
import numpy as np
import pandas as pd
from src.config import FACTORY_LOCATIONS, STATE_COORDINATES, SHIPPING_MODE_SPECS


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on the earth in miles.
    """
    if pd.isna(lat1) or pd.isna(lon1) or pd.isna(lat2) or pd.isna(lon2):
        return 0.0

    R = 3958.8  # Earth radius in miles

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 1)


def calculate_route_summary(df: pd.DataFrame, min_shipments: int = 5) -> pd.DataFrame:
    """
    Aggregates route-level statistics and calculates a normalized, volume-fair
    Route Efficiency Index (REI).
    
    Route Efficiency Index (REI, 0-100 scale):
    Combines:
    1. Operational Speed (Distance / Total Lead Time): 35% weight
    2. Profit Margin Efficiency (Gross Margin %): 35% weight
    3. On-Time Delivery Rate (%): 30% weight
    
    Guards against small-sample noise by flagging or filtering low shipment counts.
    """
    if df.empty:
        return pd.DataFrame()

    route_grp = df.groupby(["Route", "Factory", "State/Province", "Region"]).agg(
        Shipments=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Order_Value=("Sales", "mean"),
        Avg_Fulfillment_Days=("Fulfillment Days", "mean"),
        Avg_Transit_Days=("Transit Days", "mean"),
        Avg_Total_Lead_Time=("Total Lead Time", "mean"),
        Avg_Distance_Miles=("Distance Miles", "mean"),
        On_Time_Shipments=("On Time", "sum")
    ).reset_index()

    route_grp["Profit_Margin_Pct"] = (
        route_grp["Total_Profit"] / route_grp["Total_Sales"].replace(0, np.nan)
    ) * 100
    route_grp["Profit_Margin_Pct"] = route_grp["Profit_Margin_Pct"].fillna(0).clip(0, 100)

    route_grp["On_Time_Rate_Pct"] = (
        route_grp["On_Time_Shipments"] / route_grp["Shipments"]
    ) * 100

    # Operational Speed: Miles traveled per day of lead time
    route_grp["Transit_Speed_Miles_Per_Day"] = (
        route_grp["Avg_Distance_Miles"] / route_grp["Avg_Total_Lead_Time"].replace(0, np.nan)
    ).fillna(0)

    # Normalize speed across routes (0 to 100)
    max_speed = route_grp["Transit_Speed_Miles_Per_Day"].max()
    min_speed = route_grp["Transit_Speed_Miles_Per_Day"].min()
    speed_range = (max_speed - min_speed) if (max_speed - min_speed) > 0 else 1.0

    route_grp["Speed_Score"] = (
        (route_grp["Transit_Speed_Miles_Per_Day"] - min_speed) / speed_range
    ) * 100

    # Composite Route Efficiency Index (REI)
    # Balanced 35% Speed + 35% Profit Margin + 30% On-Time SLA
    route_grp["Efficiency Score"] = (
        0.35 * route_grp["Speed_Score"] +
        0.35 * route_grp["Profit_Margin_Pct"] +
        0.30 * route_grp["On_Time_Rate_Pct"]
    ).round(2)

    # Flag routes with small sample size
    route_grp["Is_Reliable"] = route_grp["Shipments"] >= min_shipments

    return route_grp


def generate_dynamic_recommendations(df: pd.DataFrame) -> list[dict]:
    """
    Generates intelligent, data-driven operational observations based on
    actual statistics in the filtered dataset, instead of static text.
    """
    if df.empty:
        return []

    recommendations = []

    # 1. On-Time SLA Performance Check
    on_time_rate = (df["On Time"].sum() / len(df)) * 100
    if on_time_rate < 85.0:
        worst_mode = df.groupby("Ship Mode")["On Time"].mean().idxmin()
        worst_mode_rate = df.groupby("Ship Mode")["On Time"].mean().min() * 100
        recommendations.append({
            "type": "warning",
            "title": "Delivery SLA At Risk",
            "text": f"Overall on-time delivery rate is {on_time_rate:.1f}%. '{worst_mode}' exhibits the lowest compliance at {worst_mode_rate:.1f}%. Prioritize carrier review for this service tier."
        })
    else:
        recommendations.append({
            "type": "success",
            "title": "Healthy Delivery Reliability",
            "text": f"Network on-time fulfillment stands at {on_time_rate:.1f}%, beating standard distributor SLA benchmark (85%)."
        })

    # 2. Factory Lead Time Bottleneck
    factory_fulfillment = df.groupby("Factory")["Fulfillment Days"].mean()
    if len(factory_fulfillment) > 1:
        slowest_factory = factory_fulfillment.idxmax()
        slowest_val = factory_fulfillment.max()
        fastest_factory = factory_fulfillment.idxmin()
        fastest_val = factory_fulfillment.min()
        gap = slowest_val - fastest_val
        if gap > 1.0:
            recommendations.append({
                "type": "warning",
                "title": f"Fulfillment Disparity at {slowest_factory}",
                "text": f"{slowest_factory} averages {slowest_val:.1f} days dispatch time vs {fastest_val:.1f} days at {fastest_factory} (gap of {gap:.1f} days). Recommend warehouse workflow audit."
            })

    # 3. Profit Margin & Regional Opportunity
    region_margins = (df.groupby("Region")["Gross Profit"].sum() / df.groupby("Region")["Sales"].sum()) * 100
    best_region = region_margins.idxmax()
    lowest_region = region_margins.idxmin()
    recommendations.append({
        "type": "info",
        "title": "Margin Optimization Potential",
        "text": f"Regional gross margin ranges from {region_margins[lowest_region]:.1f}% in {lowest_region} to {region_margins[best_region]:.1f}% in {best_region}. Focus product promotions in {best_region} to maximize retained earnings."
    })

    # 4. Long Distance Route Congestion
    long_routes = df[df["Distance Miles"] > 1800]
    if len(long_routes) > 50:
        long_on_time = (long_routes["On Time"].sum() / len(long_routes)) * 100
        recommendations.append({
            "type": "info",
            "title": "Cross-Country Route Strategy",
            "text": f"Long-haul corridors (>1,800 miles) account for {len(long_routes):,} shipments with {long_on_time:.1f}% on-time rate. Consider forward-stocking high-velocity SKUs in regional 3PL hubs."
        })

    return recommendations
