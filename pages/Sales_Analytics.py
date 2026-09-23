import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    <h1>💰 Commercial & Sales Analytics</h1>
    <p>Product Portfolio Profitability • Regional Demand Distribution • Service Tier Performance</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.markdown("### 🔍 Commercial Filters")

regions = sorted(df["Region"].unique())
selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)

factories = sorted(df["Factory"].unique())
selected_factories = st.sidebar.multiselect(
    "Manufacturing Plant",
    factories,
    default=factories
)

ship_modes = sorted(df["Ship Mode"].unique())
selected_ship = st.sidebar.multiselect(
    "Shipping Service Tier",
    ship_modes,
    default=ship_modes
)

# Apply filters
filtered = df[
    (df["Region"].isin(selected_regions)) &
    (df["Factory"].isin(selected_factories)) &
    (df["Ship Mode"].isin(selected_ship))
]

if filtered.empty:
    st.warning("No records match the current filter selection.")
    st.stop()

# =====================================================
# KPI SUMMARY CARDS
# =====================================================

total_sales = filtered["Sales"].sum()
total_profit = filtered["Gross Profit"].sum()
total_orders = len(filtered)
avg_order_val = filtered["Sales"].mean()
gross_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Revenue", f"${total_sales:,.0f}")

with c2:
    st.metric("Gross Profit", f"${total_profit:,.0f}")

with c3:
    st.metric("Gross Margin", f"{gross_margin:.1f}%")

with c4:
    st.metric("Average Order Value", f"${avg_order_val:.2f}")

st.markdown("---")

# =====================================================
# MONTHLY SALES TREND (FIXED TITLE & AXES BUG)
# =====================================================

st.markdown("### 📈 Monthly Sales Revenue Trend")

monthly = (
    filtered.groupby(filtered["Order Date"].dt.to_period("M"))
    .agg(Sales=("Sales", "sum"), Profit=("Gross Profit", "sum"))
    .reset_index()
)
monthly["Order Month"] = monthly["Order Date"].astype(str)

fig_monthly = px.line(
    monthly,
    x="Order Month",
    y="Sales",
    markers=True,
    template="plotly_white",
    color_discrete_sequence=[COLORS["primary"]]
)

fig_monthly.update_traces(line=dict(width=3), marker=dict(size=7))
fig_monthly.update_layout(
    height=400,
    title="Monthly Revenue Trend (2024 - 2025)",
    xaxis_title="Order Month",
    yaxis_title="Gross Sales ($)",
    margin=dict(l=40, r=30, t=40, b=40)
)

st.plotly_chart(fig_monthly, use_container_width=True)

st.markdown("---")

# =====================================================
# REGIONAL BREAKDOWN & SHIPPING MODE DISTRIBUTION
# =====================================================

left, right = st.columns(2)

with left:
    st.markdown("### 🌍 Regional Sales Contribution")
    region_sales = (
        filtered.groupby("Region")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig_reg = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        text_auto="$,.0f",
        color="Sales",
        color_continuous_scale=[[0, "#93C5FD"], [1, COLORS["primary"]]],
        template="plotly_white"
    )
    fig_reg.update_layout(height=380, coloraxis_showscale=False)
    st.plotly_chart(fig_reg, use_container_width=True)

with right:
    st.markdown("### 📦 Order Volume by Shipping Mode")
    ship_data = (
        filtered["Ship Mode"]
        .value_counts()
        .reset_index()
    )
    ship_data.columns = ["Ship Mode", "Orders"]

    fig_pie = px.pie(
        ship_data,
        names="Ship Mode",
        values="Orders",
        hole=0.55,
        color_discrete_sequence=COLORS["chart_palette"],
        template="plotly_white"
    )
    fig_pie.update_traces(textinfo="percent+label")
    fig_pie.update_layout(height=380, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# =====================================================
# TOP SELLING PRODUCTS & SALES BY FACTORY
# =====================================================

col_prod, col_fac = st.columns([3, 2])

with col_prod:
    st.markdown("### 🏆 Top 10 Revenue Generating Products")
    top_products = (
        filtered.groupby("Product Name")
        .agg(Sales=("Sales", "sum"), Profit=("Gross Profit", "sum"), Units=("Units", "sum"))
        .sort_values("Sales", ascending=False)
        .head(10)
        .reset_index()
    )

    fig_top_prod = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        color="Profit",
        color_continuous_scale=[[0, "#A7F3D0"], [1, COLORS["accent_green"]]],
        text_auto="$,.0f",
        template="plotly_white"
    )
    fig_top_prod.update_layout(
        height=450,
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Sales ($)",
        yaxis_title="Product",
        coloraxis_colorbar=dict(title="Profit ($)")
    )
    st.plotly_chart(fig_top_prod, use_container_width=True)

with col_fac:
    st.markdown("### 🏭 Revenue by Origin Factory")
    fac_sales = (
        filtered.groupby("Factory")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_fac = px.bar(
        fac_sales,
        x="Factory",
        y="Sales",
        text_auto="$,.0f",
        color_discrete_sequence=[COLORS["secondary"]],
        template="plotly_white"
    )
    fig_fac.update_layout(
        height=450,
        xaxis_title="Manufacturing Plant",
        yaxis_title="Revenue ($)"
    )
    st.plotly_chart(fig_fac, use_container_width=True)

st.markdown("---")

# =====================================================
# SAFE SCATTER PLOT: SALES VS GROSS PROFIT
# =====================================================

st.markdown("### 📊 Order Value vs. Gross Profit Correlation")

# Safe bubble sizing by Units rather than possibly negative profit
fig_scatter = px.scatter(
    filtered,
    x="Sales",
    y="Gross Profit",
    color="Region",
    size="Units",
    hover_data=["Product Name", "Factory", "State/Province"],
    color_discrete_sequence=COLORS["chart_palette"],
    template="plotly_white"
)

fig_scatter.update_layout(
    height=450,
    xaxis_title="Order Sales ($)",
    yaxis_title="Gross Profit ($)",
    margin=dict(l=40, r=30, t=30, b=40)
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# =====================================================
# MEANINGFUL COMMERCIAL GAUGE: GROSS MARGIN %
# =====================================================

col_g1, col_g2 = st.columns([1, 2])

with col_g1:
    st.markdown("### 🎯 Portfolio Margin Health")
    fig_margin_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(gross_margin, 1),
        number={"suffix": "%"},
        title={"text": "Gross Margin %"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": COLORS["accent_green"]},
            "steps": [
                {"range": [0, 40], "color": "#FEE2E2"},
                {"range": [40, 60], "color": "#FEF3C7"},
                {"range": [60, 100], "color": "#DCFCE7"}
            ],
            "threshold": {
                "line": {"color": "#1E3A8A", "width": 3},
                "thickness": 0.75,
                "value": 60.0
            }
        }
    ))
    fig_margin_gauge.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_margin_gauge, use_container_width=True)

with col_g2:
    st.markdown("### 📋 Regional Commercial Summary Table")
    reg_summary = (
        filtered.groupby("Region")
        .agg(
            Orders=("Order ID", "count"),
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Gross Profit", "sum"),
            Avg_Order_Value=("Sales", "mean")
        )
        .reset_index()
    )
    reg_summary["Gross Margin %"] = (
        reg_summary["Total_Profit"] / reg_summary["Total_Sales"] * 100
    ).round(1)

    reg_summary_display = reg_summary.rename(columns={
        "Total_Sales": "Revenue ($)",
        "Total_Profit": "Profit ($)",
        "Avg_Order_Value": "Avg Order ($)"
    })

    st.dataframe(
        reg_summary_display.style.format({
            "Revenue ($)": "${:,.0f}",
            "Profit ($)": "${:,.0f}",
            "Avg Order ($)": "${:,.2f}",
            "Gross Margin %": "{:.1f}%",
            "Orders": "{:,}"
        }),
        use_container_width=True,
        hide_index=True
    )

# Export Sales Report
st.markdown("---")
sales_csv = filtered.to_csv(index=False)
st.download_button(
    "📥 Download Filtered Sales Report (CSV)",
    sales_csv,
    "nassau_candy_sales_report.csv",
    "text/csv"
)
