import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.theme import apply_theme
from src.data_loader import load_clean_data
from src.logistics import calculate_route_summary
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
    <h1>🚚 Shipping Route Efficiency Analytics</h1>
    <p>Corridor Velocity • Route Efficiency Index (REI) • Bottleneck Identification</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.markdown("### 🔍 Route Filters")

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

min_orders = st.sidebar.slider(
    "Minimum Route Shipment Threshold",
    min_value=1,
    max_value=25,
    value=5,
    help="Filters out low-volume corridors to eliminate small-sample noise."
)

filtered = df[
    (df["Factory"].isin(selected_factories)) &
    (df["Region"].isin(selected_regions))
]

if filtered.empty:
    st.warning("No records match the current filter selection.")
    st.stop()

# =====================================================
# ROUTE SUMMARY COMPUTATION (REI)
# =====================================================

route_summary = calculate_route_summary(filtered, min_shipments=min_orders)
reliable_routes = route_summary[route_summary["Is_Reliable"]].copy()

total_corridors = filtered["Route"].nunique()
active_reliable = len(reliable_routes)
avg_total_lead = filtered["Total Lead Time"].mean()
avg_transit = filtered["Transit Days"].mean()
network_rei = reliable_routes["Efficiency Score"].mean() if not reliable_routes.empty else 0.0

# =====================================================
# KPI CARDS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Corridors", f"{total_corridors:,}", delta=f"{active_reliable} Qualified (N>={min_orders})", delta_color="off")

with c2:
    st.metric("Total Shipments", f"{len(filtered):,}")

with c3:
    st.metric("Avg In-Transit Time", f"{avg_transit:.1f} Days", delta=f"Total Lead: {avg_total_lead:.1f} Days", delta_color="off")

with c4:
    st.metric("Network Route Index (REI)", f"{network_rei:.1f} / 100", delta="Scale: 0 - 100", delta_color="off")

st.markdown("---")

# =====================================================
# TOP & BOTTOM ROUTE RANKINGS
# =====================================================

st.markdown("### 🏆 Route Efficiency Index (REI) Rankings")
st.caption("The Route Efficiency Index (REI) normalizes operational speed (miles/day), profit margin %, and on-time compliance into a 0–100 score.")

if not reliable_routes.empty:
    top10 = reliable_routes.nlargest(10, "Efficiency Score").sort_values("Efficiency Score", ascending=True)
    bottom10 = reliable_routes.nsmallest(10, "Efficiency Score").sort_values("Efficiency Score", ascending=True)

    col_chart_top, col_chart_bot = st.columns(2)

    with col_chart_top:
        st.markdown("**Top 10 Most Efficient Corridors**")
        fig_top = px.bar(
            top10,
            x="Efficiency Score",
            y="Route",
            orientation="h",
            color="Efficiency Score",
            color_continuous_scale=[[0, "#A7F3D0"], [1, COLORS["accent_green"]]],
            text_auto=".1f",
            template="plotly_white"
        )
        fig_top.update_layout(
            height=450,
            title="Top Corridors (High Velocity & Margin)",
            xaxis_title="Route Efficiency Index (0-100)",
            yaxis_title="Corridor",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with col_chart_bot:
        st.markdown("**Bottom 10 Corridors Requiring Attention**")
        fig_bot = px.bar(
            bottom10,
            x="Efficiency Score",
            y="Route",
            orientation="h",
            color="Efficiency Score",
            color_continuous_scale=[[0, COLORS["accent_red"]], [1, "#FED7AA"]],
            text_auto=".1f",
            template="plotly_white"
        )
        fig_bot.update_layout(
            height=450,
            title="Corridors with Sub-Optimal Performance",
            xaxis_title="Route Efficiency Index (0-100)",
            yaxis_title="Corridor",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_bot, use_container_width=True)

    # Detailed table
    with st.expander("📋 View Complete Route Breakdown Table"):
        display_cols = [
            "Route", "Shipments", "Avg_Distance_Miles", "Avg_Transit_Days",
            "Avg_Total_Lead_Time", "Profit_Margin_Pct", "On_Time_Rate_Pct", "Efficiency Score"
        ]
        st.dataframe(
            reliable_routes[display_cols].sort_values("Efficiency Score", ascending=False).rename(
                columns={
                    "Avg_Distance_Miles": "Distance (Mi)",
                    "Avg_Transit_Days": "Transit (D)",
                    "Avg_Total_Lead_Time": "Lead Time (D)",
                    "Profit_Margin_Pct": "Margin %",
                    "On_Time_Rate_Pct": "On-Time %",
                    "Efficiency Score": "REI Score"
                }
            ).style.format({
                "Distance (Mi)": "{:,.0f}",
                "Transit (D)": "{:.1f}",
                "Lead Time (D)": "{:.1f}",
                "Margin %": "{:.1f}%",
                "On-Time %": "{:.1f}%",
                "REI Score": "{:.1f}"
            }),
            use_container_width=True,
            hide_index=True
        )

else:
    st.info("No routes meet the minimum shipment threshold. Try lowering the threshold slider.")

st.markdown("---")

# =====================================================
# LEAD TIME DISTRIBUTION & VELOCITY METRICS
# =====================================================

col_dist, col_speed = st.columns(2)

with col_dist:
    st.markdown("### ⏱️ Order Lead Time Distribution")
    fig_hist = px.histogram(
        filtered,
        x="Total Lead Time",
        color="Ship Mode",
        nbins=12,
        barmode="overlay",
        color_discrete_sequence=COLORS["chart_palette"],
        template="plotly_white"
    )
    fig_hist.update_layout(
        height=380,
        xaxis_title="Total Lead Time (Days)",
        yaxis_title="Shipment Volume",
        margin=dict(l=40, r=20, t=30, b=40)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_speed:
    st.markdown("### 🚀 Distance vs. Delivery Lead Time")
    fig_dist_lead = px.scatter(
        filtered.sample(min(len(filtered), 1500), random_state=42),
        x="Distance Miles",
        y="Total Lead Time",
        color="Ship Mode",
        opacity=0.6,
        color_discrete_sequence=COLORS["chart_palette"],
        template="plotly_white"
    )
    fig_dist_lead.update_layout(
        height=380,
        xaxis_title="Route Distance (Miles)",
        yaxis_title="Total Lead Time (Days)",
        margin=dict(l=40, r=20, t=30, b=40)
    )
    st.plotly_chart(fig_dist_lead, use_container_width=True)

st.markdown("---")

# =====================================================
# CALIBRATED NETWORK EFFICIENCY GAUGE
# =====================================================

col_gauge, col_info = st.columns([1, 2])

with col_gauge:
    st.markdown("### 🎯 Average Route Score")
    fig_rei_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(network_rei, 1),
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": COLORS["primary"]},
            "steps": [
                {"range": [0, 40], "color": "#FEE2E2"},
                {"range": [40, 60], "color": "#FEF3C7"},
                {"range": [60, 100], "color": "#DCFCE7"}
            ],
            "threshold": {
                "line": {"color": "#15803D", "width": 3},
                "thickness": 0.75,
                "value": 65.0
            }
        }
    ))
    fig_rei_gauge.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_rei_gauge, use_container_width=True)

with col_info:
    st.markdown("### 💡 Route Optimization Insights")
    if not reliable_routes.empty:
        best_r = reliable_routes.loc[reliable_routes["Efficiency Score"].idxmax()]
        worst_r = reliable_routes.loc[reliable_routes["Efficiency Score"].idxmin()]
        st.success(f"""
        **Top Performing Corridor:** `{best_r['Route']}`
        * **Efficiency Score:** {best_r['Efficiency Score']:.1f} | **Volume:** {best_r['Shipments']} shipments
        * **Lead Time:** {best_r['Avg_Total_Lead_Time']:.1f} days | **Margin:** {best_r['Profit_Margin_Pct']:.1f}%
        """)
        st.warning(f"""
        **Corridor Requiring Immediate Attention:** `{worst_r['Route']}`
        * **Efficiency Score:** {worst_r['Efficiency Score']:.1f} | **Volume:** {worst_r['Shipments']} shipments
        * **Lead Time:** {worst_r['Avg_Total_Lead_Time']:.1f} days | **Margin:** {worst_r['Profit_Margin_Pct']:.1f}%
        * **Recommendation:** Investigate carrier line-haul rates and dispatch delays at origin facility.
        """)

# Export Route Analytics
st.markdown("---")
route_csv = route_summary.to_csv(index=False)
st.download_button(
    "📥 Download Route Analytics Report (CSV)",
    route_csv,
    "nassau_candy_route_summary.csv",
    "text/csv"
)
