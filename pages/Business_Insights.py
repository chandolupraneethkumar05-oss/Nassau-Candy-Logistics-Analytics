import streamlit as st
import pandas as pd
import plotly.graph_objects as go




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

st.title("💡 Business Insights Dashboard")

st.caption("Executive Decision Support System")

st.markdown("---")

st.markdown("""
<div style="
background:linear-gradient(90deg,#0f2027,#203a43,#2c5364);
padding:20px;
border-radius:15px;
color:white;
margin-bottom:20px;
">

<h2>📊 Executive Business Summary</h2>

This dashboard provides strategic insights into sales performance,
factory productivity, profitability, lead time and regional performance.
It helps management identify high-performing factories, optimize logistics,
and improve overall business efficiency.

</div>
""", unsafe_allow_html=True)


total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
total_orders = len(df)
avg_lead = df["Lead Time"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Sales", f"${total_sales:,.0f}")
c2.metric("💵 Profit", f"${total_profit:,.0f}")
c3.metric("📦 Orders", total_orders)
c4.metric("🚚 Avg Lead Time", f"{avg_lead:.2f} Days")

st.markdown("---")


best_region = df.groupby("Region")["Sales"].sum().idxmax()
worst_region = df.groupby("Region")["Sales"].sum().idxmin()

best_factory = df.groupby("Factory")["Sales"].sum().idxmax()
worst_factory = df.groupby("Factory")["Sales"].sum().idxmin()

fastest_factory = df.groupby("Factory")["Lead Time"].mean().idxmin()
slowest_factory = df.groupby("Factory")["Lead Time"].mean().idxmax()

st.header("📊 Executive Insights")

left, right = st.columns(2)

with left:

    st.success(f"🏆 Best Sales Region: **{best_region}**")

    st.success(f"🏭 Best Factory: **{best_factory}**")

    st.success(f"⚡ Fastest Factory: **{fastest_factory}**")

with right:

    st.warning(f"📉 Lowest Sales Region: **{worst_region}**")

    st.warning(f"🏭 Lowest Performing Factory: **{worst_factory}**")

    st.warning(f"🐢 Slowest Factory: **{slowest_factory}**")

st.markdown("---")

score = total_profit / avg_lead

score = max(0, min(score, 100))

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    title={"text": "Overall Business Efficiency"},
    gauge={
        "axis": {"range": [0,100]},
        "bar": {"color": "green"},
        "steps": [
            {"range": [0,40], "color":"red"},
            {"range": [40,70], "color":"orange"},
            {"range": [70,100], "color":"limegreen"}
        ]
    }
))

st.plotly_chart(fig, use_container_width=True)


st.markdown("---")

st.header("🤖 Strategic Recommendations")

st.success("""
### 🚀 Recommendation 1

Increase production in the highest-performing factory to maximize revenue.
""")

st.warning("""
### ⏳ Recommendation 2

Reduce average lead time on low-efficiency routes.
""")

st.info("""
### 📈 Recommendation 3

Expand business in the highest-profit regions.
""")

st.error("""
### ⚠ Recommendation 4

Monitor factories with low profitability and high lead times.
""")


st.markdown("---")

st.header("📋 Executive Management Summary")

summary = pd.DataFrame({

"Key Metric":[

"Total Orders",
"Total Sales",
"Gross Profit",
"Average Lead Time",
"Factories",
"Regions"

],

"Value":[

len(df),
f"${total_sales:,.0f}",
f"${total_profit:,.0f}",
round(avg_lead,2),
df["Factory"].nunique(),
df["Region"].nunique()

]

})

st.dataframe(summary, use_container_width=True)

st.markdown("---")

csv = summary.to_csv(index=False)

st.download_button(

"⬇ Download Executive Report",

csv,

"Executive_Report.csv",

"text/csv"

)

