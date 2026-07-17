import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.kpi-card{
background:linear-gradient(135deg,#0f172a,#1e293b);
padding:22px;
border-radius:18px;
border-left:6px solid #38bdf8;
box-shadow:0 8px 25px rgba(0,0,0,.35);
transition:all .3s ease;
margin-bottom:18px;
}

.kpi-card:hover{
transform:translateY(-6px);
box-shadow:0 15px 35px rgba(56,189,248,.35);
}

.kpi-title{
font-size:20px;
font-weight:600;
color:#cbd5e1;
margin-bottom:12px;
}

.kpi-value{
font-size:42px;
font-weight:800;
color:white;
margin-bottom:8px;
}

.kpi-sub{
font-size:14px;
color:#94a3b8;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/cleaned_dataset.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    return df

df = load_data()

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="header-box">

<h1>🍬 Nassau Candy Distributor</h1>

<h3>Factory-to-Customer Shipping Route Efficiency Analytics</h3>

</div>
""", unsafe_allow_html=True)

st.caption(
    f"Dashboard Generated : {datetime.now().strftime('%d %B %Y  %I:%M %p')}"
)

st.markdown("---")

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.image(
    "https://img.icons8.com/color/96/factory.png",
    width=80
)

st.sidebar.title("Dashboard Filters")

# Date

min_date = df["Order Date"].min()
max_date = df["Order Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date,max_date)
)

# Region

selected_region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

# Factory

selected_factory = st.sidebar.multiselect(
    "Factory",
    sorted(df["Factory"].unique()),
    default=sorted(df["Factory"].unique())
)

# Ship Mode

selected_ship = st.sidebar.multiselect(
    "Ship Mode",
    sorted(df["Ship Mode"].unique()),
    default=sorted(df["Ship Mode"].unique())
)

# State

selected_state = st.sidebar.multiselect(
    "State",
    sorted(df["State/Province"].unique()),
    default=sorted(df["State/Province"].unique())
)

# ============================================================
# FILTER DATA
# ============================================================

filtered = df.copy()

if len(date_range)==2:

    start=pd.to_datetime(date_range[0])
    end=pd.to_datetime(date_range[1])

    filtered=filtered[
        (filtered["Order Date"]>=start) &
        (filtered["Order Date"]<=end)
    ]

filtered=filtered[
    filtered["Region"].isin(selected_region)
]

filtered=filtered[
    filtered["Factory"].isin(selected_factory)
]

filtered=filtered[
    filtered["Ship Mode"].isin(selected_ship)
]

filtered=filtered[
    filtered["State/Province"].isin(selected_state)
]

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_orders=len(filtered)

total_sales=filtered["Sales"].sum()

total_profit=filtered["Gross Profit"].sum()

avg_lead=filtered["Lead Time"].mean()

factory_count=filtered["Factory"].nunique()

state_count=filtered["State/Province"].nunique()

route_count=filtered.groupby(
    ["Factory","State/Province"]
).ngroups

average_order=filtered["Sales"].mean()



# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.markdown(
    """
    <div style="
        background: linear-gradient(90deg,#0f2027,#203a43,#2c5364);
        padding:18px;
        border-radius:15px;
        color:white;
        margin-bottom:20px;
    ">
        <h2>📈 Executive Summary</h2>

        This dashboard provides a real-time overview of Nassau Candy Distributor's
        shipping performance, factory productivity, route efficiency,
        sales performance and logistics KPIs.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# KPI CARDS
# ============================================================

row1 = st.columns(4)

with row1[0]:
    st.metric(
        label="📦 Total Orders",
        value=f"{total_orders:,}"
    )

with row1[1]:
    st.metric(
        label="💰 Total Sales",
        value=f"${total_sales:,.0f}"
    )

with row1[2]:
    st.metric(
        label="💵 Gross Profit",
        value=f"${total_profit:,.0f}"
    )

with row1[3]:
    st.metric(
        label="🚚 Avg Lead Time",
        value=f"{avg_lead:.2f} Days"
    )

row2 = st.columns(4)

with row2[0]:
    st.metric(
        label="🏭 Factories",
        value=factory_count
    )

with row2[1]:
    st.metric(
        label="🗺️ States",
        value=state_count
    )

with row2[2]:
    st.metric(
        label="🛣️ Routes",
        value=route_count
    )

with row2[3]:
    st.metric(
        label="🛒 Avg Order Value",
        value=f"${average_order:,.0f}"
    )

st.markdown("---")



# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.header("💡 Executive Insights")

best_region = filtered.groupby("Region")["Sales"].sum().idxmax()
worst_region = filtered.groupby("Region")["Sales"].sum().idxmin()

best_factory = filtered.groupby("Factory")["Sales"].sum().idxmax()
worst_factory = filtered.groupby("Factory")["Sales"].sum().idxmin()

fastest_factory = filtered.groupby("Factory")["Lead Time"].mean().idxmin()
slowest_factory = filtered.groupby("Factory")["Lead Time"].mean().idxmax()

col1, col2 = st.columns(2)

with col1:
    st.success(f"🏆 Best Sales Region: **{best_region}**")
    st.success(f"🏭 Best Factory: **{best_factory}**")
    st.success(f"⚡ Fastest Factory: **{fastest_factory}**")

with col2:
    st.warning(f"📉 Lowest Sales Region: **{worst_region}**")
    st.warning(f"🏭 Lowest Performing Factory: **{worst_factory}**")
    st.warning(f"🐢 Slowest Factory: **{slowest_factory}**")
    

# ============================================================
# DATASET SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📋 Dataset Summary")

summary = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Factories",
        "Regions",
        "States",
        "Products",
        "Ship Modes"
    ],
    "Value": [
        len(filtered),
        filtered["Factory"].nunique(),
        filtered["Region"].nunique(),
        filtered["State/Province"].nunique(),
        filtered["Product Name"].nunique(),
        filtered["Ship Mode"].nunique()
    ]
})

st.dataframe(summary, use_container_width=True, hide_index=True)


# ============================================================
# DATA PREVIEW
# ============================================================

with st.expander("📄 Preview Filtered Dataset"):
    st.dataframe(filtered.head(20), use_container_width=True)



# ============================================================
# ANALYTICS DASHBOARD
# ============================================================

st.header("📊 Sales & Logistics Analytics")

# ------------------------------------------------------------
# Monthly Sales Trend
# ------------------------------------------------------------

monthly_sales = (
    filtered.groupby(filtered["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    template="plotly_dark",
    title="📈 Monthly Sales Trend",
)

fig.update_traces(
    line=dict(color="#00E5FF", width=4),
    marker=dict(size=8)
)

fig.update_layout(
    title_x=0.5,
    height=450
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# TWO CHARTS
# ============================================================

left, right = st.columns(2)

# ------------------------------------------------------------
# Ship Mode Distribution
# ------------------------------------------------------------

with left:

    ship = (
        filtered["Ship Mode"]
        .value_counts()
        .reset_index()
    )

    ship.columns = ["Ship Mode","Orders"]

    fig = px.pie(
        ship,
        names="Ship Mode",
        values="Orders",
        hole=0.60,
        template="plotly_dark",
        title="📦 Ship Mode Distribution"
    )

    fig.update_traces(textinfo="percent+label")

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# Sales by Region
# ------------------------------------------------------------

with right:

    region = (
        filtered.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        region,
        x="Region",
        y="Sales",
        color="Sales",
        text_auto=".2s",
        template="plotly_dark",
        title="🌍 Sales by Region"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# FACTORY PERFORMANCE
# ============================================================

factory = (
    filtered.groupby("Factory")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    factory,
    x="Factory",
    y="Sales",
    color="Sales",
    text_auto=".2s",
    template="plotly_dark",
    title="🏭 Factory Performance"
)

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# PROFIT + MONTHLY ORDERS
# ============================================================

left,right = st.columns(2)

# ------------------------------------------------------------
# Profit
# ------------------------------------------------------------

with left:

    profit = (
        filtered.groupby("Region")["Gross Profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        profit,
        x="Region",
        y="Gross Profit",
        color="Gross Profit",
        text_auto=".2s",
        template="plotly_dark",
        title="💰 Gross Profit by Region"
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# Monthly Orders
# ------------------------------------------------------------

with right:

    orders = (
        filtered.groupby(
            filtered["Order Date"].dt.to_period("M")
        )
        .size()
        .reset_index(name="Orders")
    )

    orders["Order Date"] = orders["Order Date"].astype(str)

    fig = px.area(
        orders,
        x="Order Date",
        y="Orders",
        template="plotly_dark",
        title="📦 Monthly Orders"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# TOP PRODUCTS
# ============================================================

st.subheader("🏆 Top 10 Best Selling Products")

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
    text_auto=".2s",
    template="plotly_dark"
)

fig.update_layout(
    height=550,
    yaxis={'categoryorder':'total ascending'}
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")



# ============================================================
# ROUTE ANALYTICS
# ============================================================

st.header("🚚 Route Efficiency Analytics")

filtered = filtered.copy()

filtered["Route"] = (
    filtered["Factory"] +
    " ➜ " +
    filtered["State/Province"]
)

route_summary = (
    filtered.groupby("Route")
    .agg(
        Shipments=("Order ID", "count"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Avg_Lead_Time=("Lead Time", "mean")
    )
    .reset_index()
)

route_summary["Efficiency Score"] = (
    route_summary["Profit"] /
    route_summary["Avg_Lead_Time"]
)

route_summary = route_summary.fillna(0)

top10 = route_summary.nlargest(10, "Efficiency Score")
bottom10 = route_summary.nsmallest(10, "Efficiency Score")

left, right = st.columns(2)

with left:

    fig = px.bar(
        top10,
        x="Efficiency Score",
        y="Route",
        orientation="h",
        color="Efficiency Score",
        template="plotly_dark",
        title="🏆 Top 10 Efficient Routes"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.bar(
        bottom10,
        x="Efficiency Score",
        y="Route",
        orientation="h",
        color="Efficiency Score",
        template="plotly_dark",
        title="⚠ Bottom 10 Efficient Routes"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")


# ============================================================
# FACTORY LOCATION MAP
# ============================================================

st.header("🗺 Factory Network")

factory_map = folium.Map(
    location=[39, -98],
    zoom_start=4,
    tiles="CartoDB Positron"
)

factories = (
    filtered[
        [
            "Factory",
            "Factory Latitude",
            "Factory Longitude"
        ]
    ]
    .drop_duplicates()
)

for _, row in factories.iterrows():

    folium.CircleMarker(
        location=[
            row["Factory Latitude"],
            row["Factory Longitude"]
        ],
        radius=9,
        popup=f"<b>{row['Factory']}</b>",
        tooltip=row["Factory"],
        color="green",
        fill=True,
        fill_opacity=0.8
    ).add_to(factory_map)

st_folium(factory_map, width=None, height=600)



# ============================================================
# LOGISTICS EFFICIENCY
# ============================================================

st.header("📈 Logistics Efficiency Score")

score = (
    filtered["Gross Profit"].sum()
    /
    filtered["Lead Time"].mean()
)

score = max(0, min(score, 100))

fig = go.Figure(go.Indicator(

    mode="gauge+number",

    value=score,

    number={'suffix': "%"},

    title={"text":"Overall Efficiency"},

    gauge={

        "axis":{"range":[0,100]},

        "bar":{"color":"limegreen"},

        "steps":[

            {"range":[0,40],"color":"#ff4d4d"},

            {"range":[40,70],"color":"orange"},

            {"range":[70,100],"color":"#00cc66"}

        ]
    }

))

fig.update_layout(height=450)

st.plotly_chart(fig, use_container_width=True)


# ============================================================
# AI-LIKE RECOMMENDATIONS
# ============================================================

st.header("💡 Executive Recommendations")

col1, col2, col3 = st.columns(3)

with col1:

    st.success("""
### 🚀 Recommendation

Increase shipments from the highest-performing factory to improve logistics efficiency.
""")

with col2:

    st.warning("""
### ⏳ Recommendation

Reduce lead time on the lowest-performing routes to improve customer satisfaction.
""")

with col3:

    st.info("""
### 📈 Recommendation

Focus on expanding sales in high-profit regions while monitoring slower factories.
""")
    
    
# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("---")

csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Dataset",
    csv,
    file_name="filtered_dataset.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
"""
<div style="text-align:center; padding:20px;">

<h3>🍬 Nassau Candy Distributor Analytics Platform</h3>

<p><b>Factory-to-Customer Shipping Route Efficiency Analysis</b></p>

<p>
Built with ❤️ using
Python • Streamlit • Plotly • Folium • Pandas
</p>

<p>© 2026 Logistics Analytics Dashboard</p>

</div>
""",
unsafe_allow_html=True
)

# ============================================================
# ROUTE SUMMARY KPIs
# ============================================================

st.subheader("🚚 Route Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Routes", len(route_summary))
c2.metric("Top Route Score", f"{top10['Efficiency Score'].max():.2f}")
c3.metric("Average Route Score", f"{route_summary['Efficiency Score'].mean():.2f}")
c4.metric("Average Shipments", f"{route_summary['Shipments'].mean():.1f}")