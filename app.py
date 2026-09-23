import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy Logistics Analytics",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# MULTIPAGE NAVIGATION
# ============================================================

pages = {
    "Overview": [
        st.Page(
            "pages/Home.py",
            title="Executive Portal",
            icon="🏢",
            default=True
        ),
        st.Page(
            "pages/Executive_Dashboard.py",
            title="Executive Dashboard",
            icon="📊"
        ),
    ],

    "Operational Analytics": [
        st.Page(
            "pages/Route_Analytics.py",
            title="Route Efficiency",
            icon="🚚"
        ),
        st.Page(
            "pages/Factory_Analytics.py",
            title="Factory Performance",
            icon="🏭"
        ),
        st.Page(
            "pages/Sales_Analytics.py",
            title="Commercial & Sales",
            icon="💰"
        ),
    ],

    "Intelligence & ML": [
        st.Page(
            "pages/Predictive_Analytics.py",
            title="Predictive Lead Time (ML)",
            icon="🔮"
        ),
        st.Page(
            "pages/Business_Insights.py",
            title="Strategic Insights",
            icon="💡"
        ),
    ],
}

# ============================================================
# RUN NAVIGATION
# ============================================================

pg = st.navigation(
    pages,
    position="sidebar",
    expanded=True
)

pg.run()