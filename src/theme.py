"""
Nassau Candy Logistics Analytics - Natural Corporate Theme & Visualization Engine
Provides clean, human-designed corporate aesthetics with organic, accessible colors.
No AI-template dark neon, electric cyan glows, or generic styling.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
from src.config import COLORS

# ==============================================================================
# CSS FOR STREAMLIT (Natural, Executive, Human-Designed)
# ==============================================================================
CORPORATE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], [class*="st-"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Page Background */
.stApp {
    background-color: #F8FAFC;
    color: #0F172A;
}

/* Top Navigation / Header */
.main-header {
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    padding: 24px 32px;
    margin: -1rem -1rem 1.5rem -1rem;
    border-radius: 0 0 12px 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.main-header h1 {
    font-size: 26px;
    font-weight: 700;
    color: #1E3A8A;
    margin: 0;
    letter-spacing: -0.02em;
}

.main-header p {
    font-size: 14px;
    color: #64748B;
    margin: 4px 0 0 0;
}

/* Natural KPI Metric Cards */
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 20px 22px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    transition: all 0.2s ease;
    height: 100%;
}

.metric-card:hover {
    border-color: #CBD5E1;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
}

.metric-title {
    font-size: 13px;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.metric-subtitle {
    font-size: 12px;
    font-weight: 500;
    color: #059669;
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.metric-subtitle.neutral {
    color: #64748B;
}

.metric-subtitle.warning {
    color: #D97706;
}

/* Clean Section Containers */
.section-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}

/* Callout Boxes */
.callout-box {
    border-left: 4px solid #1E3A8A;
    background: #F1F5F9;
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    margin: 16px 0;
    color: #1E293B;
}

.callout-box.success {
    border-left-color: #15803D;
    background: #F0FDF4;
    color: #14532D;
}

.callout-box.warning {
    border-left-color: #D97706;
    background: #FFFBEB;
    color: #78350F;
}

.callout-box.info {
    border-left-color: #2563EB;
    background: #EFF6FF;
    color: #1E3A8A;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0;
}

/* Streamlit Native Metric Customization */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 14px 18px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}

div[data-testid="stMetricLabel"] {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #64748B !important;
    text-transform: uppercase;
}

div[data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
}

/* Dataframe styling */
div[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    overflow: hidden;
}

/* Footer */
.corporate-footer {
    text-align: center;
    padding: 32px 16px;
    font-size: 13px;
    color: #64748B;
    border-top: 1px solid #E2E8F0;
    margin-top: 48px;
}
</style>
"""


def apply_theme():
    """Injects the natural corporate CSS into the current Streamlit page."""
    st.markdown(CORPORATE_CSS, unsafe_allow_html=True)


def configure_plotly_theme():
    """Sets a clean, accessible corporate Plotly theme as default."""
    corporate_template = go.layout.Template()
    corporate_template.layout = go.Layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#0F172A", size=12),
        colorway=COLORS["chart_palette"],
        margin=dict(l=40, r=30, t=50, b=40),
        xaxis=dict(
            showgrid=True,
            gridcolor="#F1F5F9",
            linecolor="#CBD5E1",
            tickfont=dict(color="#475569", size=11),
            title=dict(font=dict(color="#0F172A", size=12))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F1F5F9",
            linecolor="#CBD5E1",
            tickfont=dict(color="#475569", size=11),
            title=dict(font=dict(color="#0F172A", size=12))
        ),
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=12,
            font_family="Plus Jakarta Sans, sans-serif",
            font_color="#FFFFFF"
        )
    )
    pio.templates["corporate_clean"] = corporate_template
    pio.templates.default = "corporate_clean"


# Execute layout template registration upon import
configure_plotly_theme()
