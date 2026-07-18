import streamlit as st
import pandas as pd
import plotly.express as px



# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_dataset.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    return df

df = load_data()

# =====================================================
# PAGE TITLE
# =====================================================

st.title("💰 Sales Analytics Dashboard")

st.caption("Complete Sales Performance Analysis")

st.markdown("---")


# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Sales Filters")

regions = sorted(df["Region"].unique())

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)

factories = sorted(df["Factory"].unique())

selected_factories = st.sidebar.multiselect(
    "Factory",
    factories,
    default=factories
)

ship_modes = sorted(df["Ship Mode"].unique())

selected_ship = st.sidebar.multiselect(
    "Ship Mode",
    ship_modes,
    default=ship_modes
)

filtered = df[
    (df["Region"].isin(selected_regions)) &
    (df["Factory"].isin(selected_factories)) &
    (df["Ship Mode"].isin(selected_ship))
]


# =====================================================
# KPI CARDS
# =====================================================

sales = filtered["Sales"].sum()
profit = filtered["Gross Profit"].sum()
orders = len(filtered)
avg_sale = filtered["Sales"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Sales", f"${sales:,.0f}")
c2.metric("💵 Gross Profit", f"${profit:,.0f}")
c3.metric("📦 Orders", f"{orders:,}")
c4.metric("🛒 Avg Order", f"${avg_sale:,.2f}")

st.markdown("---")


st.markdown("""
<div style="
background:linear-gradient(90deg,#0f2027,#203a43,#2c5364);
padding:18px;
border-radius:15px;
color:white;
margin-bottom:20px;
">
<h2>📈 Executive Sales Summary</h2>

This dashboard provides a complete view of sales performance across factories,
regions and shipping modes. Use the filters to identify high-performing
markets, profitable factories and sales trends.

</div>
""", unsafe_allow_html=True)


# =====================================================
# MONTHLY SALES TREND
# =====================================================

st.subheader("📈 Monthly Sales Trend")

monthly = (
    filtered.groupby(filtered["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly["Order Date"] = monthly["Order Date"].astype(str)

fig = px.line(
    monthly,
    x="Order Date",
    y="Sales",
    markers=True,
    template="plotly_dark",
    color_discrete_sequence=["cyan"]
)

fig.update_layout(
    height=500,
    title="🏭 Factory-wise Sales Performance",
    title_x=0.5,
    xaxis_title="Factory",
    yaxis_title="Sales ($)"
)


st.plotly_chart(fig, use_container_width=True)


st.markdown("---")

left, right = st.columns(2)

with left:

    region_sales = (
        filtered.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Sales",
        template="plotly_dark",
        title="Sales by Region"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    ship = (
        filtered["Ship Mode"]
        .value_counts()
        .reset_index()
    )

    ship.columns = ["Ship Mode", "Orders"]

    fig = px.pie(
        ship,
        names="Ship Mode",
        values="Orders",
        hole=.55,
        template="plotly_dark",
        title="Orders by Ship Mode"
    )

    st.plotly_chart(fig, use_container_width=True)
    
st.markdown("---")
st.subheader("🏭 Sales by Factory")

factory_sales = (
    filtered.groupby("Factory")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    factory_sales,
    x="Factory",
    y="Sales",
    color="Sales",
    template="plotly_dark",
    text_auto=".2s"
)

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🏆 Top 10 Selling Products")

top_products = (
    filtered.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    template="plotly_dark",
    text_auto=".2s"
)

fig.update_layout(
    height=600,
    title="🏆 Top 10 Selling Products",
    title_x=0.5,
    xaxis_title="Sales ($)",
    yaxis_title="Products",
    yaxis={"categoryorder": "total ascending"}
)

fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.subheader("📊 Sales vs Gross Profit")

fig = px.scatter(
    filtered,
    x="Sales",
    y="Gross Profit",
    color="Region",
    size="Gross Profit",
    hover_data=["Factory", "State/Province"],
    template="plotly_dark"
)

fig.update_layout(height=600)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📅 Monthly Orders")

monthly_orders = (
    filtered.groupby(filtered["Order Date"].dt.to_period("M"))
    .size()
    .reset_index(name="Orders")
)

monthly_orders["Order Date"] = monthly_orders["Order Date"].astype(str)

fig = px.area(
    monthly_orders,
    x="Order Date",
    y="Orders",
    template="plotly_dark"
)

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.subheader("💡 Executive Sales Insights")

best_region = filtered.groupby("Region")["Sales"].sum().idxmax()
best_factory = filtered.groupby("Factory")["Sales"].sum().idxmax()
best_product = filtered.groupby("Product Name")["Sales"].sum().idxmax()

c1, c2, c3 = st.columns(3)

with c1:
    st.success(f"""
### 🌎 Best Sales Region

**{best_region}**
""")

with c2:
    st.success(f"""
### 🏭 Best Performing Factory

**{best_factory}**
""")

with c3:
    st.success(f"""
### 🏆 Best Selling Product

**{best_product}**
""")


st.markdown("---")
st.subheader("📋 Sales Summary")

summary = (
    filtered.groupby("Region")
    .agg(
        Total_Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Orders=("Order ID", "count"),
        Avg_Order=("Sales", "mean")
    )
    .reset_index()
)

st.dataframe(summary, use_container_width=True)

st.markdown("---")

import plotly.graph_objects as go

st.markdown("---")
st.subheader("🎯 Overall Sales Performance")

sales_score = min((sales / df["Sales"].sum()) * 100, 100)

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=sales_score,
    number={"suffix": "%"},
    title={"text": "Sales Performance Score"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#00E5FF"},
        "steps": [
            {"range": [0, 40], "color": "#ef4444"},
            {"range": [40, 70], "color": "#f59e0b"},
            {"range": [70, 100], "color": "#22c55e"}
        ]
    }
))

fig.update_layout(height=420)

st.plotly_chart(fig, use_container_width=True)

csv = filtered.to_csv(index=False)

st.download_button(
    "⬇ Download Sales Report",
    csv,
    "Sales_Report.csv",
    "text/csv"
)
