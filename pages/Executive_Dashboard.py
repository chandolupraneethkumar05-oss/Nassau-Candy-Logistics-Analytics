import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from src.theme import apply_theme
from src.data_loader import load_clean_data
from src.logistics import calculate_route_summary, generate_dynamic_recommendations
from src.config import COLORS

# Apply natural corporate styling
apply_theme()

# Load clean dataset
df = load_clean_data()

# ============================================================
# EXECUTIVE HEADER
# ============================================================

st.markdown("""
<div class="executive-header">
    <h1>📊 Executive Logistics Dashboard</h1>
    <p>Unified Operational Overview • Supply Chain Fulfillment & Commercial Performance</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("### 🔍 Dashboard Filters")

# Date Filter
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region Filter
all_regions = sorted(df["Region"].unique())
selected_regions = st.sidebar.multiselect(
    "Region",
    all_regions,
    default=all_regions
)

# Factory Filter
all_factories = sorted(df["Factory"].unique())
selected_factories = st.sidebar.multiselect(
    "Origin Factory",
    all_factories,
    default=all_factories
)

# Ship Mode Filter
all_modes = sorted(df["Ship Mode"].unique())
selected_modes = st.sidebar.multiselect(
    "Service Tier / Ship Mode",
    all_modes,
    default=all_modes
)

# ============================================================
# FILTER DATASET
# ============================================================

filtered = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_dt = pd.to_datetime(date_range[0])
    end_dt = pd.to_datetime(date_range[1])
    filtered = filtered[(filtered["Order Date"] >= start_dt) & (filtered["Order Date"] <= end_dt)]

if selected_regions:
    filtered = filtered[filtered["Region"].isin(selected_regions)]

if selected_factories:
    filtered = filtered[filtered["Factory"].isin(selected_factories)]

if selected_modes:
    filtered = filtered[filtered["Ship Mode"].isin(selected_modes)]

if filtered.empty:
    st.warning("No records match the current filter selection. Please adjust your filters.")
    st.stop()

# ============================================================
# EXECUTIVE KPI SUMMARY CARDS
# ============================================================

total_orders = len(filtered)
total_sales = filtered["Sales"].sum()
total_profit = filtered["Gross Profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0

avg_lead = filtered["Total Lead Time"].mean()
avg_fulfillment = filtered["Fulfillment Days"].mean()
avg_transit = filtered["Transit Days"].mean()
avg_distance = filtered["Distance Miles"].mean()
on_time_pct = (filtered["On Time"].mean() * 100)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="Total Orders",
        value=f"{total_orders:,}",
        delta=f"{filtered['Units'].sum():,} Units"
    )

with kpi2:
    st.metric(
        label="Gross Revenue",
        value=f"${total_sales:,.0f}",
        delta=f"Margin: {profit_margin:.1f}%"
    )

with kpi3:
    st.metric(
        label="Gross Profit",
        value=f"${total_profit:,.0f}",
        delta=f"Avg Order: ${filtered['Sales'].mean():.2f}",
        delta_color="normal"
    )

with kpi4:
    st.metric(
        label="On-Time Delivery Rate",
        value=f"{on_time_pct:.1f}%",
        delta="Target: 85.0%",
        delta_color="normal" if on_time_pct >= 85.0 else "inverse"
    )

st.markdown("<br>", unsafe_allow_html=True)

kpi5, kpi6, kpi7, kpi8 = st.columns(4)

with kpi5:
    st.metric(
        label="Total Lead Time",
        value=f"{avg_lead:.1f} Days",
        delta="Order to Delivery",
        delta_color="off"
    )

with kpi6:
    st.metric(
        label="Plant Dispatch Delay",
        value=f"{avg_fulfillment:.1f} Days",
        delta="Order to Ship",
        delta_color="off"
    )

with kpi7:
    st.metric(
        label="In-Transit Duration",
        value=f"{avg_transit:.1f} Days",
        delta="Ship to Customer",
        delta_color="off"
    )

with kpi8:
    st.metric(
        label="Average Route Distance",
        value=f"{avg_distance:,.0f} Mi",
        delta=f"{filtered['Route'].nunique()} Active Routes",
        delta_color="off"
    )

st.markdown("---")

# ============================================================
# MONTHLY REVENUE & FULFILLMENT TRENDS
# ============================================================

col_trend, col_otif = st.columns([2, 1])

with col_trend:
    st.markdown("### 📈 Monthly Revenue & Order Volume")
    monthly = filtered.groupby(filtered["Order Date"].dt.to_period("M")).agg(
        Sales=("Sales", "sum"),
        Orders=("Order ID", "count")
    ).reset_index()
    monthly["Month"] = monthly["Order Date"].astype(str)

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=monthly["Month"],
        y=monthly["Sales"],
        name="Revenue ($)",
        marker_color=COLORS["primary"],
        yaxis="y"
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly["Month"],
        y=monthly["Orders"],
        name="Order Volume",
        mode="lines+markers",
        line=dict(color=COLORS["accent_warm"], width=3),
        marker=dict(size=6),
        yaxis="y2"
    ))
    fig_trend.update_layout(
        template="plotly_white",
        height=380,
        margin=dict(l=40, r=40, t=30, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="#F1F5F9"),
        yaxis2=dict(title="Orders", overlaying="y", side="right", showgrid=False)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_otif:
    st.markdown("### 🎯 Network On-Time Delivery (OTIF)")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(on_time_pct, 1),
        number={'suffix': "%", 'font': {'size': 36, 'color': '#0F172A'}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#CBD5E1"},
            "bar": {"color": COLORS["primary"]},
            "steps": [
                {"range": [0, 60], "color": "#FEE2E2"},
                {"range": [60, 85], "color": "#FEF3C7"},
                {"range": [85, 100], "color": "#DCFCE7"}
            ],
            "threshold": {
                "line": {"color": "#B91C1C", "width": 3},
                "thickness": 0.75,
                "value": 85.0
            }
        }
    ))
    fig_gauge.update_layout(
        template="plotly_white",
        height=300,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.caption("Threshold line at 85% represents industry target SLA benchmark.")

st.markdown("---")

# ============================================================
# REGIONAL BREAKDOWN & FACTORY PERFORMANCE
# ============================================================

col_reg, col_fact = st.columns(2)

with col_reg:
    st.markdown("### 🌍 Regional Sales & Profitability")
    reg_df = filtered.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Lead_Time=("Total Lead Time", "mean")
    ).reset_index().sort_values("Sales", ascending=False)

    fig_reg = px.bar(
        reg_df,
        x="Region",
        y=["Sales", "Profit"],
        barmode="group",
        color_discrete_sequence=[COLORS["primary"], COLORS["accent_green"]],
        template="plotly_white",
        labels={"value": "Amount ($)", "variable": "Metric"}
    )
    fig_reg.update_layout(height=350, margin=dict(l=40, r=20, t=30, b=40))
    st.plotly_chart(fig_reg, use_container_width=True)

with col_fact:
    st.markdown("### 🏭 Factory Lead Time & Volume Distribution")
    fact_df = filtered.groupby("Factory").agg(
        Orders=("Order ID", "count"),
        Fulfillment=("Fulfillment Days", "mean"),
        Transit=("Transit Days", "mean")
    ).reset_index().sort_values("Orders", ascending=True)

    fig_fact = px.bar(
        fact_df,
        y="Factory",
        x=["Fulfillment", "Transit"],
        orientation="h",
        barmode="stack",
        color_discrete_sequence=[COLORS["secondary"], COLORS["accent_warm"]],
        template="plotly_white",
        labels={"value": "Days", "variable": "Duration Component"}
    )
    fig_fact.update_layout(height=350, margin=dict(l=40, r=20, t=30, b=40))
    st.plotly_chart(fig_fact, use_container_width=True)

st.markdown("---")

# ============================================================
# ROUTE EFFICIENCY INDEX (REI) RANKINGS
# ============================================================

st.markdown("### 🚚 High-Volume Corridor Performance (Route Efficiency Index)")

route_summary = calculate_route_summary(filtered, min_shipments=5)
reliable_routes = route_summary[route_summary["Is_Reliable"]].copy()

if not reliable_routes.empty:
    top5_routes = reliable_routes.nlargest(5, "Efficiency Score")
    bottom5_routes = reliable_routes.nsmallest(5, "Efficiency Score")

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.markdown("**Top 5 Efficient Corridors**")
        st.dataframe(
            top5_routes[["Route", "Shipments", "Avg_Distance_Miles", "Avg_Total_Lead_Time", "Profit_Margin_Pct", "Efficiency Score"]].rename(
                columns={
                    "Avg_Distance_Miles": "Distance (Mi)",
                    "Avg_Total_Lead_Time": "Lead Time (D)",
                    "Profit_Margin_Pct": "Margin %",
                    "Efficiency Score": "REI Score"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

    with col_t2:
        st.markdown("**Bottom 5 Corridors Requiring Review**")
        st.dataframe(
            bottom5_routes[["Route", "Shipments", "Avg_Distance_Miles", "Avg_Total_Lead_Time", "Profit_Margin_Pct", "Efficiency Score"]].rename(
                columns={
                    "Avg_Distance_Miles": "Distance (Mi)",
                    "Avg_Total_Lead_Time": "Lead Time (D)",
                    "Profit_Margin_Pct": "Margin %",
                    "Efficiency Score": "REI Score"
                }
            ),
            use_container_width=True,
            hide_index=True
        )
else:
    st.info("Insufficient route volume under current filters to compute reliable rankings (N >= 5).")

st.markdown("---")

# ============================================================
# FACTORY NETWORK MAP
# ============================================================

st.markdown("### 🗺️ Manufacturing Facility Network")

map_center = [39.5, -98.35]
net_map = folium.Map(location=map_center, zoom_start=4, tiles="CartoDB Positron")

factory_coords = filtered[[
    "Factory", "Factory Latitude", "Factory Longitude"
]].drop_duplicates()

for _, row in factory_coords.iterrows():
    fact_name = row["Factory"]
    fact_orders = len(filtered[filtered["Factory"] == fact_name])
    fact_sales = filtered[filtered["Factory"] == fact_name]["Sales"].sum()
    fact_avg_lead = filtered[filtered["Factory"] == fact_name]["Total Lead Time"].mean()

    popup_html = f"""
    <div style="font-family: sans-serif; font-size: 12px; width: 180px;">
        <h4 style="margin: 0 0 6px 0; color: #1E3A8A;">{fact_name}</h4>
        <b>Orders:</b> {fact_orders:,}<br>
        <b>Sales:</b> ${fact_sales:,.0f}<br>
        <b>Avg Lead Time:</b> {fact_avg_lead:.1f} Days
    </div>
    """

    folium.CircleMarker(
        location=[row["Factory Latitude"], row["Factory Longitude"]],
        radius=10,
        popup=folium.Popup(popup_html, max_width=220),
        tooltip=fact_name,
        color="#1E3A8A",
        fill=True,
        fill_color="#2563EB",
        fill_opacity=0.85
    ).add_to(net_map)

st_folium(net_map, height=450, width=None)

st.markdown("---")

# ============================================================
# DATA-DRIVEN OPERATIONAL OBSERVATIONS
# ============================================================

st.markdown("### 💡 Data-Driven Operational Observations")

recommendations = generate_dynamic_recommendations(filtered)

rec_cols = st.columns(len(recommendations)) if recommendations else [st.container()]
for i, rec in enumerate(recommendations):
    col = rec_cols[i] if i < len(rec_cols) else st
    with col:
        box_class = rec["type"]
        st.markdown(f"""
        <div class="callout-box {box_class}">
            <strong>{rec['title']}</strong><br>
            <span style="font-size:13px;">{rec['text']}</span>
        </div>
        """, unsafe_allow_html=True)

# Export Filtered Data
st.markdown("---")
csv_data = filtered.to_csv(index=False)
st.download_button(
    label="📥 Export Filtered Dataset (CSV)",
    data=csv_data,
    file_name="nassau_candy_executive_extract.csv",
    mime="text/csv"
)