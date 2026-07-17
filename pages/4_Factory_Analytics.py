import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Factory Analytics",
    page_icon="🏭",
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

st.title("🏭 Factory Analytics Dashboard")
st.caption("Factory Performance & Productivity Analysis")

st.markdown("---")


st.sidebar.header("Factory Filters")

factory = st.sidebar.multiselect(
    "Factory",
    sorted(df["Factory"].unique()),
    default=sorted(df["Factory"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

filtered = df[
    (df["Factory"].isin(factory)) &
    (df["Region"].isin(region))
]


sales = filtered["Sales"].sum()
profit = filtered["Gross Profit"].sum()
lead = filtered["Lead Time"].mean()
factories = filtered["Factory"].nunique()

c1,c2,c3,c4 = st.columns(4)

c1.metric("🏭 Factories", factories)
c2.metric("💰 Sales", f"${sales:,.0f}")
c3.metric("💵 Profit", f"${profit:,.0f}")
c4.metric("🚚 Avg Lead Time", f"{lead:.2f}")


st.markdown("---")

factory_summary = (
    filtered.groupby("Factory")
    .agg(
        Orders=("Order ID","count"),
        Sales=("Sales","sum"),
        Profit=("Gross Profit","sum"),
        Avg_Lead_Time=("Lead Time","mean")
    )
    .reset_index()
)

st.subheader("📋 Factory Performance Summary")

st.dataframe(
    factory_summary,
    use_container_width=True
)


st.markdown("---")

st.subheader("💰 Sales by Factory")

fig = px.bar(
    factory_summary,
    x="Factory",
    y="Sales",
    color="Sales",
    text_auto=".2s",
    template="plotly_dark"
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

st.subheader("📈 Profit by Factory")

fig = px.bar(
    factory_summary,
    x="Factory",
    y="Profit",
    color="Profit",
    text_auto=".2s",
    template="plotly_dark"
)
fig.update_layout(
    height=500,
    title="💰 Factory Profit Comparison",
    title_x=0.5,
    xaxis_title="Factory",
    yaxis_title="Gross Profit ($)"
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("---")

st.subheader("🚚 Average Lead Time")

fig = px.bar(
    factory_summary,
    x="Factory",
    y="Avg_Lead_Time",
    color="Avg_Lead_Time",
    text_auto=".2f",
    template="plotly_dark"
)

fig.update_layout(
    height=500,
    title="🚚 Average Lead Time by Factory",
    title_x=0.5,
    xaxis_title="Factory",
    yaxis_title="Lead Time (Days)"
)
st.plotly_chart(fig, use_container_width=True)


st.markdown("---")

st.subheader("🗺 Factory Locations")

factory_map = folium.Map(
    location=[39,-98],
    zoom_start=4,
    tiles="CartoDB Positron"
)

locations = filtered[
    [
        "Factory",
        "Factory Latitude",
        "Factory Longitude"
    ]
].drop_duplicates()

for _,row in locations.iterrows():

    folium.CircleMarker(
    location=[
        row["Factory Latitude"],
        row["Factory Longitude"]
    ],
    radius=10,
    tooltip=row["Factory"],
    popup=f"""
    <b>{row['Factory']}</b><br>
    Factory Location
    """,
    color="darkblue",
    fill=True,
    fill_color="cyan",
    fill_opacity=0.9
).add_to(factory_map)
st_folium(factory_map,height=600,width=None)


st.markdown("---")

best_factory = (
    factory_summary.sort_values(
        "Sales",
        ascending=False
    ).iloc[0]
)

st.success(f"""
## 🏆 Best Performing Factory

**Factory:** {best_factory['Factory']}

**Sales:** ${best_factory['Sales']:,.0f}

**Profit:** ${best_factory['Profit']:,.0f}

**Average Lead Time:** {best_factory['Avg_Lead_Time']:.2f} Days
""")


st.markdown("---")

st.markdown("---")

st.subheader("💡 Executive Factory Insights")

highest_profit = factory_summary.loc[
    factory_summary["Profit"].idxmax(),
    "Factory"
]

fastest_factory = factory_summary.loc[
    factory_summary["Avg_Lead_Time"].idxmin(),
    "Factory"
]

highest_orders = factory_summary.loc[
    factory_summary["Orders"].idxmax(),
    "Factory"
]

c1, c2, c3 = st.columns(3)

with c1:
    st.success(f"""
### 🏭 Highest Profit

**{highest_profit}**
""")

with c2:
    st.info(f"""
### 🚚 Fastest Factory

**{fastest_factory}**
""")

with c3:
    st.warning(f"""
### 📦 Highest Orders

**{highest_orders}**
""")
    

st.markdown("---")
st.subheader("🎯 Factory Performance Score")

score = min((profit / df["Gross Profit"].sum()) * 100, 100)

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    number={"suffix": "%"},
    title={"text": "Overall Factory Performance"},
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

csv = factory_summary.to_csv(index=False)

st.download_button(
    "⬇ Download Factory Report",
    csv,
    "Factory_Report.csv",
    "text/csv"
)


