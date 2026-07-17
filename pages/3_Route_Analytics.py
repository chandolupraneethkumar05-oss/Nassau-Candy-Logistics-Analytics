import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Route Analytics",
    page_icon="🚚",
    layout="wide"
)

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

# Create Route Column
df["Route"] = (
    df["Factory"] +
    " ➜ " +
    df["State/Province"]
)

st.title("🚚 Route Analytics Dashboard")
st.caption("Factory-to-Customer Route Efficiency Analysis")

st.markdown("---")


st.sidebar.header("Route Filters")

selected_factory = st.sidebar.multiselect(
    "Factory",
    sorted(df["Factory"].unique()),
    default=sorted(df["Factory"].unique())
)

selected_region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

filtered = df[
    (df["Factory"].isin(selected_factory)) &
    (df["Region"].isin(selected_region))
]


total_routes = filtered["Route"].nunique()
avg_lead = filtered["Lead Time"].mean()
total_shipments = len(filtered)
best_profit = filtered["Gross Profit"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("🛣 Routes", total_routes)
c2.metric("📦 Shipments", total_shipments)
c3.metric("🚚 Avg Lead Time", f"{avg_lead:.2f}")
c4.metric("💰 Total Profit", f"${best_profit:,.0f}")

st.markdown("---")


# =====================================================
# ROUTE SUMMARY
# =====================================================

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


st.header("🏆 Route Performance")

top10 = route_summary.nlargest(10, "Efficiency Score")
bottom10 = route_summary.nsmallest(10, "Efficiency Score")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Efficient Routes")
    st.dataframe(top10, use_container_width=True)

with col2:
    st.subheader("Bottom 10 Efficient Routes")
    st.dataframe(bottom10, use_container_width=True)


st.markdown("---")
st.subheader("📊 Top 10 Route Efficiency")

fig = px.bar(
    top10,
    x="Efficiency Score",
    y="Route",
    orientation="h",
    color="Efficiency Score",
    template="plotly_dark",
    text_auto=".2f"
)

fig.update_layout(
    height=600,
    title="🏆 Top 10 Most Efficient Routes",
    title_x=0.5,
    xaxis_title="Efficiency Score",
    yaxis_title="Factory → State"
)

fig.update_layout(
    height=450,
    title="📈 Overall Route Efficiency Score",
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.subheader("🚚 Lead Time Distribution")

fig = px.histogram(
    filtered,
    x="Lead Time",
    nbins=40,
    color="Region",
    template="plotly_dark"
)

fig.update_layout(
    height=500,
    title="🚚 Lead Time Distribution",
    title_x=0.5,
    xaxis_title="Lead Time (Days)",
    yaxis_title="Number of Shipments"
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.subheader("🏭 Factory Performance")

factory = (
    filtered.groupby("Factory")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum"),
        Lead_Time=("Lead Time", "mean")
    )
    .reset_index()
)

fig = px.scatter(
    factory,
    x="Sales",
    y="Profit",
    size="Lead_Time",
    color="Factory",
    template="plotly_dark",
    hover_name="Factory"
)

fig.update_layout(
    height=600,
    title="🏭 Factory Performance Analysis",
    title_x=0.5,
    xaxis_title="Sales ($)",
    yaxis_title="Gross Profit ($)"
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("---")
st.subheader("📈 Overall Route Efficiency")

score = route_summary["Efficiency Score"].mean()

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    title={"text": "Average Efficiency Score"},
    gauge={
        "axis": {"range": [0, 120]},
        "bar": {"color": "limegreen"},
        "steps": [
            {"range": [0, 40], "color": "#ff4b4b"},
            {"range": [40, 80], "color": "#ffa500"},
            {"range": [80, 120], "color": "#00cc66"},
        ],
    },
))

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")


st.markdown("---")

st.subheader("💡 Executive Route Insights")

best_route = route_summary.loc[
    route_summary["Efficiency Score"].idxmax(),
    "Route"
]

worst_route = route_summary.loc[
    route_summary["Efficiency Score"].idxmin(),
    "Route"
]

fastest_factory = (
    filtered.groupby("Factory")["Lead Time"]
    .mean()
    .idxmin()
)

c1, c2, c3 = st.columns(3)

with c1:
    st.success(f"""
### 🏆 Best Route

**{best_route}**
""")

with c2:
    st.warning(f"""
### ⚠ Needs Improvement

**{worst_route}**
""")

with c3:
    st.info(f"""
### 🚚 Fastest Factory

**{fastest_factory}**
""")

csv = route_summary.to_csv(index=False)

st.download_button(
    "⬇ Download Route Report",
    csv,
    "Route_Report.csv",
    "text/csv"
)


