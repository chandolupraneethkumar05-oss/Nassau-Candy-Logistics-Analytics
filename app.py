import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy Analytics",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# MULTIPAGE NAVIGATION
# ============================================================

pages = {
    "Dashboard": [
        st.Page(
            "pages/Home.py",
            title="Home",
            icon="🏠",
            default=True
        ),
        st.Page(
            "pages/Executive_Dashboard.py",
            title="Executive Dashboard",
            icon="📊"
        ),
    ],

    "Analytics": [
        st.Page(
            "pages/Sales_Analytics.py",
            title="Sales Analytics",
            icon="💰"
        ),
        st.Page(
            "pages/Route_Analytics.py",
            title="Route Analytics",
            icon="🚚"
        ),
        st.Page(
            "pages/Factory_Analytics.py",
            title="Factory Analytics",
            icon="🏭"
        ),
    ],

    "Insights": [
        st.Page(
            "pages/Business_Insights.py",
            title="Business Insights",
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