import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Nassau Candy Analytics",
    page_icon="🍬",
    layout="wide"
)

# -------------------------------------------------
# PREMIUM CSS
# -------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html,body,[class*="css"]{
font-family:'Poppins',sans-serif;
}

.stApp{
background:linear-gradient(135deg,#07111f,#0f172a,#111827);
color:white;
}

/* Hide Streamlit Menu */

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

/* Hero */

.hero{

padding:45px;

border-radius:25px;

background:linear-gradient(135deg,#2563eb,#1e3a8a,#0f172a);

box-shadow:0px 0px 30px rgba(0,0,0,.45);

text-align:center;

margin-bottom:30px;

}

.hero h1{

font-size:54px;

color:white;

margin-bottom:10px;

}

.hero h3{

color:#cbd5e1;

font-weight:400;

}

.hero p{

font-size:20px;

color:#d1d5db;

}

/* Cards */

.card{

background:#111827;

padding:25px;

border-radius:18px;

box-shadow:0px 0px 20px rgba(0,0,0,.25);

transition:.3s;

height:260px;

}

.card:hover{

transform:translateY(-8px);

box-shadow:0px 0px 25px #2563eb;

}

.card h2{

color:#60a5fa;

}

.card ul{

line-height:2;

}

/* Feature */

.feature{

background:#1f2937;

padding:20px;

border-radius:15px;

text-align:center;

margin-top:10px;

margin-bottom:10px;

font-size:18px;

}

/* Footer */

.footer{

text-align:center;

padding:30px;

font-size:18px;

color:#cbd5e1;

}

</style>

""",unsafe_allow_html=True)




# -------------------------------------------------
# HERO
# -------------------------------------------------

st.markdown("""

<div class="hero">

<h1>🍬 Nassau Candy Distributor</h1>

<h3>Factory-to-Customer Shipping Route Efficiency Analysis</h3>

<p>

Professional Logistics Analytics Dashboard

</p>

</div>

""",unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------
# ABOUT
# -------------------------------------------------

st.header("📖 About the Project")

st.write("""

This Business Intelligence dashboard analyzes the logistics performance of Nassau Candy Distributor.

The dashboard helps management monitor:

- Factory Performance
- Route Efficiency
- Lead Time
- Sales Performance
- Gross Profit
- Business Insights

using interactive visualizations developed in Python and Streamlit.

""")

st.markdown("---")

# ============================================================
# DASHBOARD MODULES
# ============================================================

st.header("📊 Dashboard Modules")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div class="card">
    <h2>📊 Executive Dashboard</h2>

    <ul>
    <li>KPI Cards</li>
    <li>Sales Overview</li>
    <li>Profit Overview</li>
    <li>Lead Time Analysis</li>
    <li>Business Summary</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h2>🚚 Route Analytics</h2>

    <ul>
    <li>Best Routes</li>
    <li>Worst Routes</li>
    <li>Efficiency Analysis</li>
    <li>Lead Time</li>
    <li>Performance Ranking</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h2>💡 Business Insights</h2>

    <ul>
    <li>Executive Summary</li>
    <li>Recommendations</li>
    <li>Risk Areas</li>
    <li>Business KPIs</li>
    <li>Final Report</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="card">
    <h2>💰 Sales Analytics</h2>

    <ul>
    <li>Monthly Sales</li>
    <li>Regional Sales</li>
    <li>Profit Analysis</li>
    <li>Sales Trends</li>
    <li>Interactive Charts</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h2>🏭 Factory Analytics</h2>

    <ul>
    <li>Factory Ranking</li>
    <li>Factory Map</li>
    <li>Sales Performance</li>
    <li>Lead Time</li>
    <li>Profit Analysis</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# KEY FEATURES
# ============================================================

st.header("⭐ Key Features")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.success("📊 Interactive Dashboard")

with c2:
    st.success("🚚 Route Optimization")

with c3:
    st.success("🏭 Factory Performance")

with c4:
    st.success("📈 Business Intelligence")

c5, c6, c7, c8 = st.columns(4)

with c5:
    st.info("🗺 Interactive Maps")

with c6:
    st.info("📥 CSV Export")

with c7:
    st.info("⚡ Real-Time Filters")

with c8:
    st.info("📉 Profit Analysis")

st.markdown("---")

# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.header("⚙ Technology Stack")

t1, t2, t3, t4 = st.columns(4)

t1.metric("🐍 Python", "3.x")
t2.metric("📊 Streamlit", "Latest")
t3.metric("📈 Plotly", "Interactive")
t4.metric("🗺 Folium", "Maps")

t5, t6, t7 = st.columns(3)

t5.metric("🐼 Pandas", "Analysis")
t6.metric("🔢 NumPy", "Computing")
t7.metric("🤖 Scikit-Learn", "Analytics")

st.markdown("---")

# ============================================================
# PROJECT STATISTICS
# ============================================================

st.header("📈 Project Statistics")

s1, s2, s3, s4 = st.columns(4)

s1.metric("📦 Orders", "10K+")
s2.metric("🏭 Factories", "5")
s3.metric("🌎 Regions", "4")
s4.metric("🗺 States", "50+")


# ============================================================
# PROJECT WORKFLOW
# ============================================================

st.markdown("---")

st.header("📌 Project Workflow")

workflow_col1, workflow_col2 = st.columns([1, 2])

with workflow_col1:
    st.markdown("""
### 🔄 Process Flow

📂 Raw Dataset

⬇

🧹 Data Cleaning

⬇

📊 Data Analysis

⬇

📈 Interactive Visualization

⬇

🚚 Route Optimization

⬇

💡 Business Insights
""")

with workflow_col2:

    st.info("""
### 📖 Workflow Description

This dashboard transforms raw logistics data into meaningful business insights.

The complete workflow includes:

• Data Cleaning and Preprocessing

• Exploratory Data Analysis

• KPI Generation

• Factory Performance Evaluation

• Route Efficiency Analysis

• Sales and Profit Analysis

• Interactive Visualizations

• Executive Decision Support
""")

st.markdown("---")

# ============================================================
# WHY THIS PROJECT?
# ============================================================

st.header("🎯 Why This Dashboard?")

left, right = st.columns(2)

with left:

    st.success("""
### 🚀 Business Benefits

✔ Improve Shipping Efficiency

✔ Reduce Lead Time

✔ Increase Profitability

✔ Identify Best Performing Factories

✔ Improve Decision Making

✔ Monitor Logistics Performance
""")

with right:

    st.warning("""
### 📊 Dashboard Capabilities

✔ Interactive KPIs

✔ Dynamic Charts

✔ Factory Maps

✔ Route Analysis

✔ Business Recommendations

✔ Download Reports
""")

st.markdown("---")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

<hr style="border:1px solid #374151;">

<h3>🍬 Nassau Candy Distributor Analytics Dashboard</h3>

<p>
Factory-to-Customer Shipping Route Efficiency Analysis
</p>

<p>
Developed using Python • Streamlit • Plotly • Pandas • Folium
</p>

<p>
Prepared for <b>Unified Mentor Internship Project</b>
</p>

<p>
Developed by <b>Praneeth Kumar Chandolu</b>
</p>

<p style="color:#60A5FA;">
© 2026 All Rights Reserved
</p>

</div>
""", unsafe_allow_html=True)