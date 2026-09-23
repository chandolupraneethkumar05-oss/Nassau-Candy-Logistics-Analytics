import streamlit as st
import pandas as pd
import plotly.express as px

from src.theme import apply_theme
from src.data_loader import load_clean_data
from src.ml_model import get_trained_predictor
from src.config import FACTORY_LOCATIONS, STATE_COORDINATES, COLORS
from src.logistics import haversine_distance

# Apply natural corporate styling
apply_theme()

# Load clean dataset
df = load_clean_data()

# =====================================================
# PAGE HEADER
# =====================================================

st.markdown("""
<div class="executive-header">
    <h1>🔮 Predictive Logistics & Lead Time Simulator</h1>
    <p>Machine Learning Inference • Random Forest Delivery Forecasting • SLA Delay Risk Estimation</p>
</div>
""", unsafe_allow_html=True)

# Train or retrieve cached ML model
with st.spinner("Initializing predictive machine learning pipelines..."):
    predictor = get_trained_predictor(df)

# =====================================================
# MODEL PERFORMANCE METRICS
# =====================================================

st.markdown("### 📊 Model Validation & Performance Benchmarks")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Model Architecture", "Random Forest + GBDT")

with m2:
    st.metric("Lead Time MAE", f"± {predictor.metrics['mae_days']} Days", delta="Mean Absolute Error", delta_color="off")

with m3:
    st.metric("Regression Fit ($R^2$)", f"{predictor.metrics['r2_score']:.3f}", delta="Explains 75%+ variance", delta_color="off")

with m4:
    st.metric("SLA Classification Acc.", f"{predictor.metrics['accuracy']:.1f}%", delta="On-Time vs Delay", delta_color="off")

st.markdown("---")

# =====================================================
# INTERACTIVE SHIPMENT SIMULATOR
# =====================================================

st.markdown("### 🎛️ Interactive 'What-If' Shipment Simulator")
st.write("Simulate a proposed shipment to forecast delivery duration and evaluate SLA delay risks before dispatching inventory.")

sim_col1, sim_col2 = st.columns([1, 1])

with sim_col1:
    st.markdown("#### Shipment Attributes")
    sel_factory = st.selectbox(
        "Origin Manufacturing Plant",
        options=sorted(FACTORY_LOCATIONS.keys()),
        index=0
    )

    sel_state = st.selectbox(
        "Destination State / Province",
        options=sorted(STATE_COORDINATES.keys()),
        index=sorted(STATE_COORDINATES.keys()).index("California") if "California" in STATE_COORDINATES else 0
    )

    sel_mode = st.selectbox(
        "Shipping Service Tier",
        options=["Standard Class", "Second Class", "First Class", "Same Day"],
        index=0
    )

    sel_units = st.slider(
        "Order Volume (Units / Cases)",
        min_value=1,
        max_value=25,
        value=4
    )

    # Compute exact distance for input
    f_coords = FACTORY_LOCATIONS.get(sel_factory, {"lat": 39.0, "lon": -98.0})
    s_coords = STATE_COORDINATES.get(sel_state, {"lat": 39.0, "lon": -98.0})
    dist_miles = haversine_distance(f_coords["lat"], f_coords["lon"], s_coords["lat"], s_coords["lon"])

with sim_col2:
    st.markdown("#### Real-Time Machine Learning Prediction")
    
    # Run prediction
    result = predictor.predict(
        factory=sel_factory,
        state=sel_state,
        ship_mode=sel_mode,
        units=sel_units,
        distance_miles=dist_miles
    )

    pred_lead = result["predicted_lead_time_days"]
    on_time_prob = result["on_time_probability"]
    risk_level = result["estimated_delivery_risk"]

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.metric(
            label="Predicted Lead Time",
            value=f"{pred_lead:.1f} Days",
            delta=f"Transit Distance: {dist_miles:,.0f} Mi",
            delta_color="off"
        )
    with p_col2:
        st.metric(
            label="On-Time Probability",
            value=f"{on_time_prob:.1f}%",
            delta=f"Risk Level: {risk_level}",
            delta_color="normal" if risk_level == "Low" else ("off" if risk_level == "Medium" else "inverse")
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if risk_level == "Low":
        st.success(f"""
        **Optimal Routing Confirmed:** High confidence ({on_time_prob:.1f}%) that this shipment will meet the **{sel_mode}** SLA.
        Expected delivery: **{pred_lead:.1f} days** from order placement.
        """)
    elif risk_level == "Medium":
        st.warning(f"""
        **Moderate Risk of SLA Breach:** Estimated on-time probability is **{on_time_prob:.1f}%**.
        Consider upgrading from **{sel_mode}** to **First Class** if customer requires guaranteed expedited delivery.
        """)
    else:
        st.error(f"""
        **High Delay Risk Detected:** On-time delivery chance is only **{on_time_prob:.1f}%** over this **{dist_miles:,.0f}-mile corridor**.
        Recommend sourcing from an alternative facility closer to **{sel_state}**.
        """)

st.markdown("---")

# =====================================================
# FEATURE IMPORTANCE & LEAD TIME DRIVERS
# =====================================================

st.markdown("### 🔍 Key Drivers of Delivery Duration")

# Extract feature importances from trained model
model = predictor.regression_pipeline.named_steps["model"]
preprocessor = predictor.regression_pipeline.named_steps["preprocessor"]
cat_encoder = preprocessor.named_transformers_["cat"]
cat_names = list(cat_encoder.get_feature_names_out(["Factory", "State/Province", "Ship Mode"]))
all_feature_names = cat_names + ["Units", "Distance Miles"]

importances = pd.DataFrame({
    "Feature": all_feature_names,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False).head(10)

fig_imp = px.bar(
    importances.sort_values("Importance", ascending=True),
    x="Importance",
    y="Feature",
    orientation="h",
    color="Importance",
    color_continuous_scale=[[0, "#93C5FD"], [1, COLORS["primary"]]],
    template="plotly_white",
    title="Top 10 Factors Influencing Delivery Lead Time"
)

fig_imp.update_layout(
    height=400,
    xaxis_title="Relative Feature Importance (MDI)",
    yaxis_title="Feature Name",
    coloraxis_showscale=False
)
st.plotly_chart(fig_imp, use_container_width=True)

st.caption("Feature importance calculated using Mean Decrease in Impurity (MDI) across 100 decision trees in the Random Forest ensemble.")
