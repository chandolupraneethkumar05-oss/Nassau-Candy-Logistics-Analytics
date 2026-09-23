# 🍬 Nassau Candy Distributor - Factory-to-Customer Shipping Route Efficiency Analysis

## 📌 Project Overview

This project is developed as part of the **Unified Mentor Data Analytics Internship**.

The objective of this project is to analyze the shipping operations of **Nassau Candy Distributor** and identify opportunities to improve logistics efficiency by analyzing factory-to-customer routes, sales performance, lead time, factory productivity, and overall business performance.

An interactive dashboard has been developed using **Streamlit** to provide real-time analytics and business insights.

---

# 🎯 Problem Statement

Nassau Candy Distributor operates multiple factories that ship products to customers across different regions.

Due to increasing logistics complexity, the company needs a data-driven solution to:

- Monitor shipping performance
- Reduce lead time
- Improve route efficiency
- Increase profitability
- Analyze factory performance
- Support management decision-making

---

# 🎯 Project Objectives

The main objectives of this project are:

- Analyze factory-to-customer shipping routes
- Calculate route efficiency
- Monitor sales performance
- Evaluate factory productivity
- Identify high-performing and low-performing regions
- Generate executive business insights
- Build an interactive analytics dashboard

---

# 📂 Dataset

The project uses the **Nassau Candy Distributor Dataset**.

The dataset contains information about:

- Order Details
- Shipping Information
- Factory Information
- Customer Location
- Sales
- Cost
- Gross Profit
- Lead Time
- Regions
- States
- Ship Mode

---

# 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Folium
- Streamlit-Folium
- Matplotlib
- OpenPyXL
- Scikit-Learn

---

# 📊 Dashboard Modules

## 1️⃣ Executive Dashboard

Provides an overall business overview including:

- KPI Cards
- Sales Summary
- Profit Summary
- Lead Time
- Monthly Sales Trend
- Factory Locations
- Route Efficiency
- Business Insights

---

## 2️⃣ Sales Analytics

Analyzes sales performance through:

- Total Sales
- Gross Profit
- Monthly Sales Trend
- Sales by Region
- Sales by Factory
- Top Selling Products
- Sales vs Profit Analysis
- Download Sales Report

---

## 3️⃣ Route Analytics

Analyzes logistics performance:

- Route Efficiency
- Top Efficient Routes
- Least Efficient Routes
- Lead Time Analysis
- Factory Performance
- Route Score
- Download Route Report

---

## 4️⃣ Factory Analytics

Provides factory-wise analysis:

- Factory Performance
- Sales by Factory
- Profit by Factory
- Lead Time
- Factory Locations Map
- Best Performing Factory
- Download Factory Report

---

## 5️⃣ Predictive Logistics (Machine Learning)

Leverages **Scikit-Learn** predictive pipelines:

- Random Forest Regressor for Delivery Lead Time
- Gradient Boosting Classifier for On-Time SLA Delay Risk
- Interactive "What-If" Shipment Simulator
- Feature Importance and Lead Time Driver Analysis

---

## 6️⃣ Strategic Business Insights

Provides dynamic executive-level decision support:

- Dynamic Operational Observations (Condition-Triggered)
- Balanced Supply Chain Health Index (0-100)
- Plant Dispatch Bottleneck Diagnostics
- Regional Margin Opportunities
- Executive Scorecard Download

---

# 📈 Key Features

- **Natural Corporate Theme:** Human-designed executive palette (warm slate, deep navy, forest green, warm amber) replacing AI-like neon styling.
- **Realistic Supply Chain Modeling:** Segregated plant dispatch handling (0–5 days) from carrier transit duration (1–6 days) with geodesic Haversine distance calculations.
- **Standardized Route Efficiency Index (REI):** Normalized, volume-weighted scoring combining operational velocity, gross margin %, and on-time compliance ($N \ge 5$ threshold).
- **Interactive Predictive Simulator:** Real-time ML inference for hypothetical orders.
- **Multi-Page Navigation:** Built with native Streamlit navigation.
- **Dynamic Cross-Filtering:** Interactive sidebar controls across all analytics modules.

---

# 📁 Project Structure

```
Nassau_Candy_Project/
│
├── app.py                              # Streamlit application entrypoint & navigation
├── requirements.txt                    # Project dependencies
├── README.md                           # Documentation
│
├── assets/
│   └── style.css                       # Natural corporate styling
│
├── src/                                # Core modular Python package
│   ├── __init__.py
│   ├── config.py                       # Coordinates, constants, corporate color tokens
│   ├── data_loader.py                  # Cached data loading & schema normalization
│   ├── logistics.py                    # Haversine distance, REI score, dynamic observations
│   ├── ml_model.py                     # Scikit-learn Random Forest & GBDT ML pipelines
│   └── theme.py                        # Natural corporate CSS & accessible Plotly theme
│
├── data/
│   ├── Nassau Candy Distributor.csv    # Source raw shipment transactions
│   └── cleaned_dataset.csv             # Cleaned dataset with realistic lead times & distances
│
├── pages/
│   ├── Home.py                         # Executive portal & architecture
│   ├── Executive_Dashboard.py          # Unified KPI cards, OTIF gauge, route rankings
│   ├── Route_Analytics.py              # Corridor velocity, REI rankings, distance metrics
│   ├── Factory_Analytics.py            # Plant capacity, dispatch delay, fulfillment SLA
│   ├── Sales_Analytics.py              # Product margin, monthly trend, sales distribution
│   ├── Predictive_Analytics.py         # ML shipment lead time & delay risk simulator
│   └── Business_Insights.py            # Strategic scorecard & dynamic observations
│
├── scripts/
│   ├── clean_data.py                   # Deterministic data cleaning & feature engineering
│   ├── analysis.py                     # Standardized route aggregation & REI calculation
│   ├── module4_visualization.py        # Natural corporate chart generation pipeline
│   ├── check_columns.py                # Schema inspection tool
│   └── check_dates.py                  # Date validation & lead time verification tool
│
├── charts/                             # High-resolution executive PNG charts
└── output/                             # Generated route summaries & top/bottom corridors
```

---

# ⚙ Installation

## Clone the repository

```bash
git clone <repository_url>
```

## Navigate to project folder

```bash
cd Nassau_Candy_Project
```

## Create virtual environment

```bash
python -m venv venv
```

## Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install required packages

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Project

Run the following command:

```bash
streamlit run app.py
```

The dashboard will open in your default web browser.

---

# 📊 Business Insights Generated

The dashboard helps identify:

- Best Performing Factory
- Highest Sales Region
- Lowest Sales Region
- Fastest Factory
- Slowest Factory
- Route Efficiency
- Lead Time Performance
- Sales Trends
- Profit Analysis

---

# 🚀 Future Enhancements

Future improvements can include:

- Machine Learning based sales prediction
- Route optimization using AI
- Demand forecasting
- Live shipment tracking
- Customer analytics
- Cloud deployment
- Automated PDF report generation

---

# 📷 Dashboard Preview

The dashboard consists of five interactive modules:

- Executive Dashboard
- Sales Analytics
- Route Analytics
- Factory Analytics
- Business Insights

(You may add screenshots here if required.)

---

# 📚 Learning Outcomes

During this project, the following skills were applied:

- Data Cleaning
- Data Analysis
- Data Visualization
- Business Intelligence
- Dashboard Development
- Python Programming
- Streamlit Application Development
- Logistics Performance Analysis

---

# 👨‍💻 Developed By

**Praneeth Kumar Chandolu**

Unified Mentor Internship Project

Factory-to-Customer Shipping Route Efficiency Analysis

---

# 📄 License

This project is developed for educational and internship purposes under the Unified Mentor Internship Program.