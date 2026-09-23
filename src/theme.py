"""
Nassau Candy Logistics Analytics - Natural Corporate Theme & Visualization Engine
Provides clean, human-designed corporate aesthetics with maximum text visibility,
accessible high-contrast typography, and clear visual hierarchy.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
from src.config import COLORS

# ==============================================================================
# CSS FOR STREAMLIT (High-Contrast, Crystal-Clear Text Visibility)
# ==============================================================================
CORPORATE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Force overall application font and base colors */
html, body, .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

/* Explicit high-contrast text color for all Markdown elements */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] em,
p, span, label, li {
    color: #1E293B !important;
    font-size: 14px;
    line-height: 1.6;
}

/* Clear, deep dark slate headings */
h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: #0F172A !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}

h1 { font-size: 26px !important; margin-bottom: 8px !important; }
h2 { font-size: 20px !important; margin-top: 16px !important; margin-bottom: 8px !important; }
h3 { font-size: 16px !important; margin-top: 14px !important; margin-bottom: 6px !important; }

/* Captions and subtext */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
.stCaption {
    color: #475569 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Executive Header Box */
.executive-header {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-left: 6px solid #1E3A8A !important;
    border-radius: 10px !important;
    padding: 22px 28px !important;
    margin-bottom: 22px !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06) !important;
}

.executive-header h1 {
    color: #1E3A8A !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    margin: 0 !important;
}

.executive-header p {
    color: #334155 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    margin: 6px 0 0 0 !important;
}

/* Streamlit Native Metric Cards - Clean White with Crisp Dark Text */
div[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 16px 20px !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] * {
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #475569 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
}

div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    line-height: 1.2 !important;
}

div[data-testid="stMetricDelta"],
div[data-testid="stMetricDelta"] * {
    font-size: 12px !important;
    font-weight: 600 !important;
}

/* Sidebar Styling - Crisp White with Deep Dark Slate Text */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #CBD5E1 !important;
}

section[data-testid="stSidebar"] * {
    color: #0F172A !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #1E3A8A !important;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] * {
    color: #1E293B !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}

/* Multiselect tags */
span[data-baseweb="tag"] {
    background-color: #E2E8F0 !important;
    border: 1px solid #CBD5E1 !important;
}

span[data-baseweb="tag"] * {
    color: #0F172A !important;
    font-weight: 600 !important;
}

/* Selectbox & Inputs */
div[data-baseweb="select"] * {
    color: #0F172A !important;
    background-color: #FFFFFF !important;
}

/* Card Containers */
.card-container {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 20px 22px !important;
    margin-bottom: 18px !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
}

.card-title {
    font-size: 14px !important;
    font-weight: 700 !important;
    color: #1E3A8A !important;
    text-transform: uppercase !important;
    letter-spacing: 0.03em !important;
    margin-bottom: 8px !important;
}

.card-container p {
    color: #334155 !important;
    font-size: 13px !important;
    margin: 0 !important;
}

/* Callout / Alert Boxes */
.callout-box {
    border-radius: 8px !important;
    padding: 16px 20px !important;
    margin: 14px 0 !important;
    border-left: 5px solid #1E3A8A !important;
    background-color: #F1F5F9 !important;
}

.callout-box * {
    color: #0F172A !important;
}

.callout-box.success {
    border-left-color: #15803D !important;
    background-color: #F0FDF4 !important;
}

.callout-box.warning {
    border-left-color: #D97706 !important;
    background-color: #FFFBEB !important;
}

.callout-box.info {
    border-left-color: #2563EB !important;
    background-color: #EFF6FF !important;
}

/* Streamlit Native Expander */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #1E3A8A !important;
    font-weight: 700 !important;
}

/* Tables & Dataframes */
div[data-testid="stDataFrame"] {
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    background-color: #FFFFFF !important;
}

/* Footer */
.corporate-footer {
    text-align: center !important;
    padding: 32px 16px !important;
    font-size: 13px !important;
    color: #475569 !important;
    border-top: 1px solid #E2E8F0 !important;
    margin-top: 48px !important;
}
.corporate-footer strong {
    color: #1E3A8A !important;
}
</style>
"""


def apply_theme():
    """Injects the high-contrast natural corporate CSS into the current Streamlit page."""
    st.markdown(CORPORATE_CSS, unsafe_allow_html=True)


def configure_plotly_theme():
    """Sets a clean, high-contrast, accessible corporate Plotly theme as default."""
    corporate_template = go.layout.Template()
    corporate_template.layout = go.Layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#0F172A", size=12),
        colorway=COLORS["chart_palette"],
        margin=dict(l=40, r=30, t=50, b=40),
        xaxis=dict(
            showgrid=True,
            gridcolor="#E2E8F0",
            linecolor="#94A3B8",
            tickfont=dict(color="#1E293B", size=11),
            title=dict(font=dict(color="#0F172A", size=12))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E2E8F0",
            linecolor="#94A3B8",
            tickfont=dict(color="#1E293B", size=11),
            title=dict(font=dict(color="#0F172A", size=12))
        ),
        legend=dict(
            font=dict(color="#0F172A", size=11)
        ),
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=12,
            font_family="Plus Jakarta Sans, sans-serif",
            font_color="#FFFFFF"
        )
    )
    pio.templates["corporate_clean"] = corporate_template
    pio.templates.default = "corporate_clean"


# Execute layout template registration upon import
configure_plotly_theme()
