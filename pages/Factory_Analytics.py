import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from src.theme import apply_theme
from src.data_loader import load_clean_data
from src.config import COLORS

# Apply natural corporate styling
apply_theme()

# Load clean dataset
df = load_clean_data()

# =====================================================
# PAGE HEADER
# =====================================================

st.markdown("""
<div class="executive-header">
    <h1>🏭 Factory Performance & Plant Analytics</h1>
    <p>Plant Output Capacity • Order Fulfillment Delay • Geographic Service Reach</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.markdown("### 🔍 Plant Filters")

factories = sorted(df["Factory"].unique())
selected_factories = st.sidebar.multiselect(
    "Manufacturing Plant",
    factories,
    default=factories
)

regions = sorted(df["Region"].unique())
selected_regions = st.sidebar.multiselect(
    "Destination Region",
    regions,
    default=regions
)

filtered = df[
    (df["Factory"].isin(selected_factories)) &
    (df["Region"].isin(selected_regions))
]

if filtered.empty:
    st.warning("No records match the current filter selection.")
    st.stop()

# =====================================================
# FACTORY SUMMARY KPIs
# =====================================================

total_orders = len(filtered)
total_sales = filtered["Sales"].sum()
total_profit = filtered["Gross Profit"].sum()
avg_dispatch_days = filtered["Fulfillment Days"].mean()
plant_on_time_pct = (filtered["On Time"].mean() * 100)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Active Plants", f"{filtered['Factory'].nunique()} / 5")

with k2:
    st.metric("Total Production Sales", f"${total_sales:,.0f}")

with k3:
    st.metric("Avg Dispatch Delay", f"{avg_dispatch_days:.1f} Days", delta="Order-to-Ship Handling", delta_color="off")

with k4:
    st.metric("Fulfillment On-Time Rate", f"{plant_on_time_pct:.1f}%", delta="Target: 85%", delta_color="normal" if plant_on_time_pct >= 85 else "inverse")

st.markdown("---")

# =====================================================
# FACTORY PERFORMANCE SUMMARY TABLE
# =====================================================

st.markdown("### 📋 Manufacturing Facility Performance Summary")

factory_summary = (
    filtered.groupby("Factory")
    .agg(
        Orders=("Order ID", "count"),
        Units=("Units", "sum"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Avg_Fulfillment_Days=("Fulfillment Days", "mean"),
        Avg_Transit_Days=("Transit Days", "mean"),
        Avg_Total_Lead=("Total Lead Time", "mean"),
        Avg_Distance=("Distance Miles", "mean"),
        On_Time_Pct=("On Time", "mean")
    )
    .reset_index()
)

factory_summary["Margin %"] = (factory_summary["Profit"] / factory_summary["Sales"] * 100).round(1)
factory_summary["On_Time_Pct"] = (factory_summary["On_Time_Pct"] * 100).round(1)

st.dataframe(
    factory_summary.rename(columns={
        "Avg_Fulfillment_Days": "Dispatch Delay (D)",
        "Avg_Transit_Days": "Transit Duration (D)",
        "Avg_Total_Lead": "Total Lead Time (D)",
        "Avg_Distance": "Avg Reach (Mi)",
        "On_Time_Pct": "On-Time Compliance"
    }).style.format({
        "Orders": "{:,}",
        "Units": "{:,}",
        "Sales": "${:,.0f}",
        "Profit": "${:,.0f}",
        "Dispatch Delay (D)": "{:.1f}",
        "Transit Duration (D)": "{:.1f}",
        "Total Lead Time (D)": "{:.1f}",
        "Avg Reach (Mi)": "{:,.0f}",
        "Margin %": "{:.1f}%",
        "On-Time Compliance": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# =====================================================
# FACTORY COMPARISONS: SALES, PROFIT, AND DISPATCH TIME
# =====================================================

col_f1, col_f2 = st.columns(2)

with col_f1:
    st.markdown("### 💰 Commercial Output by Factory")
    fig_fac_sales = px.bar(
        factory_summary.sort_values("Sales", ascending=False),
        x="Factory",
        y=["Sales", "Profit"],
        barmode="group",
        color_discrete_sequence=[COLORS["primary"], COLORS["accent_green"]],
        text_auto="$,.0f",
        template="plotly_white"
    )
    fig_fac_sales.update_layout(height=400, yaxis_title="Amount ($)", xaxis_title="Factory")
    st.plotly_chart(fig_fac_sales, use_container_width=True)

with col_f2:
    st.markdown("### ⏱️ Warehouse Dispatch vs. Transit Time")
    fig_lead_comp = px.bar(
        factory_summary.sort_values("Avg_Total_Lead", ascending=True),
        x="Factory",
        y=["Avg_Fulfillment_Days", "Avg_Transit_Days"],
        barmode="stack",
        color_discrete_sequence=[COLORS["secondary"], COLORS["accent_warm"]],
        text_auto=".1f",
        template="plotly_white",
        labels={"value": "Average Days", "variable": "Component"}
    )
    legend_labels = {
        "Avg_Fulfillment_Days": "Dispatch Handling Delay (Days)",
        "Avg_Transit_Days": "Carrier Transit Duration (Days)"
    }
    fig_lead_comp.for_each_trace(lambda t: t.update(name=legend_labels.get(t.name, t.name)))
    fig_lead_comp.update_layout(
        height=400,
        yaxis_title="Average Days",
        xaxis_title="Factory",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_lead_comp, use_container_width=True)

st.markdown("---")

# =====================================================
# FACTORY NETWORK MAP WITH DISPATCH RADIUS
# =====================================================

st.markdown("### 🗺️ Facility Geographic Network & Outbound Footprint")

fac_map = folium.Map(location=[39.5, -98.35], zoom_start=4, tiles="CartoDB Positron")

fac_coords = filtered[[
    "Factory", "Factory Latitude", "Factory Longitude"
]].drop_duplicates()

for _, row in fac_coords.iterrows():
    f_name = row["Factory"]
    sub = filtered[filtered["Factory"] == f_name]
    f_orders = len(sub)
    f_sales = sub["Sales"].sum()
    f_dispatch = sub["Fulfillment Days"].mean()
    f_reach = sub["Distance Miles"].mean()

    popup_text = f"""
    <b>{f_name}</b><br>
    Orders: {f_orders:,}<br>
    Revenue: ${f_sales:,.0f}<br>
    Avg Dispatch: {f_dispatch:.1f} days<br>
    Avg Reach: {f_reach:,.0f} miles
    """

    folium.CircleMarker(
        location=[row["Factory Latitude"], row["Factory Longitude"]],
        radius=11,
        popup=popup_text,
        tooltip=f_name,
        color="#1E3A8A",
        fill=True,
        fill_color="#2563EB",
        fill_opacity=0.85
    ).add_to(fac_map)

st_folium(fac_map, height=450, width=None)

st.markdown("---")

# =====================================================
# MEANINGFUL OPERATIONAL GAUGE: FULFILLMENT SLA COMPLIANCE
# =====================================================

col_g1, col_g2 = st.columns([1, 2])

with col_g1:
    st.markdown("### 🎯 Plant SLA Compliance")
    fig_fac_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(plant_on_time_pct, 1),
        number={"suffix": "%"},
        title={"text": "Plant On-Time Fulfillment"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": COLORS["primary"]},
            "steps": [
                {"range": [0, 60], "color": "#FEE2E2"},
                {"range": [60, 85], "color": "#FEF3C7"},
                {"range": [85, 100], "color": "#DCFCE7"}
            ],
            "threshold": {
                "line": {"color": "#15803D", "width": 3},
                "thickness": 0.75,
                "value": 85.0
            }
        }
    ))
    fig_fac_gauge.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_fac_gauge, use_container_width=True)

with col_g2:
    st.markdown("### 💡 Plant Operational Diagnostics")
    if not factory_summary.empty:
        best_vol_fac = factory_summary.loc[factory_summary["Orders"].idxmax()]
        fastest_disp_fac = factory_summary.loc[factory_summary["Avg_Fulfillment_Days"].idxmin()]
        slowest_disp_fac = factory_summary.loc[factory_summary["Avg_Fulfillment_Days"].idxmax()]

        st.success(f"""
        **Highest Throughput Plant:** `{best_vol_fac['Factory']}`
        * Produced **{best_vol_fac['Orders']:,} orders** (${best_vol_fac['Sales']:,.0f} revenue) with **{best_vol_fac['Margin %']:.1f}% gross margin**.
        """)
        st.info(f"""
        **Fastest Dispatch Facility:** `{fastest_disp_fac['Factory']}`
        * Averages **{fastest_disp_fac['Avg_Fulfillment_Days']:.1f} days** order-to-ship handling time.
        """)
        if slowest_disp_fac['Factory'] != fastest_disp_fac['Factory']:
            st.warning(f"""
            **Dispatch Bottleneck:** `{slowest_disp_fac['Factory']}`
            * Averages **{slowest_disp_fac['Avg_Fulfillment_Days']:.1f} days** dispatch delay. Recommend order picking and staging audit.
            """)

# Export Factory Report
st.markdown("---")
fac_csv = factory_summary.to_csv(index=False)
st.download_button(
    "📥 Download Factory Performance Report (CSV)",
    fac_csv,
    "nassau_candy_factory_summary.csv",
    "text/csv"
)
