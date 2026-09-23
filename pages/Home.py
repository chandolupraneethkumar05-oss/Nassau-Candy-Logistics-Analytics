import streamlit as st
from src.theme import apply_theme
from src.data_loader import load_clean_data

# Apply natural corporate styling
apply_theme()

# Load clean data
df = load_clean_data()

# ============================================================
# EXECUTIVE HEADER
# ============================================================

st.markdown("""
<div class="executive-header">
    <h1>🍬 Nassau Candy Distributor</h1>
    <p>Factory-to-Customer Logistics Intelligence & Supply Chain Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# PLATFORM OVERVIEW
# ============================================================

col_intro, col_stats = st.columns([3, 2])

with col_intro:
    st.markdown("""
    ### 🏢 About the Distribution Network
    **Nassau Candy Distributor** operates a multi-facility confectionery manufacturing and distribution 
    network across North America. This analytics system transforms shipment-level transaction data 
    into actionable operational intelligence for plant managers, transportation planners, and executive leadership.

    #### Key Analytical Capabilities:
    * **Fulfillment vs. Transit Segregation:** Clear separation between plant dispatch handling times and carrier in-transit durations.
    * **Route Efficiency Index (REI):** Normalized, volume-weighted scoring combining transit velocity, gross margin, and on-time compliance.
    * **SLA Performance Tracking:** Carrier evaluation against promised delivery service-level agreements across 4 shipping tiers.
    * **Predictive Lead Time Engine:** Real-time machine learning inference estimating delivery transit duration and delay risk.
    """)

with col_stats:
    st.markdown("### 📊 Operational Scope")
    s1, s2 = st.columns(2)
    s1.metric("📦 Total Orders", f"{len(df):,}")
    s2.metric("🏭 Active Plants", df["Factory"].nunique())
    
    s3, s4 = st.columns(2)
    s3.metric("🗺️ Destination States", df["State/Province"].nunique())
    s4.metric("🛣️ Active Corridors", df["Route"].nunique())

st.markdown("---")

# ============================================================
# MODULE NAVIGATION CARDS
# ============================================================

st.subheader("🧭 Functional Modules")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card-container">
        <div class="card-title">📊 Executive Dashboard</div>
        <p style="font-size:13px; color:#475569;">
            High-level operational overview summarizing gross sales, margin %, network on-time delivery rate, 
            regional trends, and factory rankings.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <div class="card-title">🏭 Factory Performance</div>
        <p style="font-size:13px; color:#475569;">
            Plant-level productivity tracking, dispatch delay benchmarks, production volumes, and geographic coverage mapping.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card-container">
        <div class="card-title">🚚 Route Efficiency</div>
        <p style="font-size:13px; color:#475569;">
            Corridor-level performance analysis utilizing the Route Efficiency Index (REI), transit speed (miles/day), and bottleneck detection.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <div class="card-title">💰 Commercial & Sales</div>
        <p style="font-size:13px; color:#475569;">
            Product portfolio profitability, regional revenue contribution, monthly volume trends, and margin spread analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card-container">
        <div class="card-title">🔮 Predictive Logistics (ML)</div>
        <p style="font-size:13px; color:#475569;">
            Machine learning 'What-If' simulation powered by Scikit-Learn predicting shipment transit duration and SLA delay probabilities.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-container">
        <div class="card-title">💡 Strategic Insights</div>
        <p style="font-size:13px; color:#475569;">
            Dynamically generated business observations identifying operational anomalies, SLA vulnerabilities, and margin opportunities.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# SYSTEM ARCHITECTURE & DATA PIPELINE
# ============================================================

st.subheader("⚙️ System Architecture & Data Lineage")

st.markdown("""
```
[Raw Order Transactions]
       │
       ▼
[Deterministic ETL Pipeline (clean_data.py)]
  ├── Date normalization & verification (2024–2025)
  ├── Factory coordinate geocoding (Lat / Lon)
  ├── Destination state centroid mapping
  ├── Geodesic Haversine distance calculation (Miles)
  ├── Separation of Fulfillment Delay (Order-to-Ship) & Transit Duration (Ship-to-Delivery)
  └── Service Level Agreement (SLA) on-time compliance tagging
       │
       ▼
[Cleaned Production Dataset (cleaned_dataset.csv)]
       │
       ├──► [Route Efficiency Engine (logistics.py)] ──► Route Efficiency Index (REI)
       ├──► [Scikit-Learn ML Pipeline (ml_model.py)]  ──► Random Forest Lead Time Predictor
       └──► [Multi-Page Streamlit Analytics UI]       ──► Corporate BI & Decision Support
```
""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="corporate-footer">
    <strong>Nassau Candy Distributor Analytics Platform</strong> • Enterprise Logistics Intelligence<br>
    Built with Python, Streamlit, Pandas, Scikit-Learn, Plotly, and Folium
</div>
""", unsafe_allow_html=True)