
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Retail Sales Forecasting",
    page_icon="📊",
    layout="wide"
)

# Project paths
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data" / "processed"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    daily_sales = pd.read_csv(
        DATA_DIR / "daily_sales.csv",
        parse_dates=["date"]
    )

    forecast = pd.read_csv(
        DATA_DIR / "forecast_results.csv",
        parse_dates=["date"]
    )

    comparison = pd.read_csv(
        DATA_DIR / "model_comparison.csv"
    )

    inventory = pd.read_csv(
        DATA_DIR / "inventory_plan.csv"
    )

    return daily_sales, forecast, comparison, inventory


try:
    daily_sales, forecast, comparison, inventory = load_data()
except FileNotFoundError as e:
    st.error(
        f"Data file not found: {e}. "
        "Please export the notebook outputs first."
    )
    st.stop()

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("Retail Analytics")
st.sidebar.caption("Sales Forecasting & Inventory Planning")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Sales Forecast",
        "Model Performance",
        "Inventory Planning"
    ]
)

st.sidebar.divider()
st.sidebar.caption(
    "Forecasting model: XGBoost Regressor"
)

# --------------------------------------------------
# 1. EXECUTIVE OVERVIEW
# --------------------------------------------------

if page == "Executive Overview":

    st.title("Executive Overview")
    st.write(
        "An overview of historical retail sales "
        "and forecasted demand across stores and product families."
    )

    total_sales = daily_sales["total_sales"].sum()
    average_daily_sales = daily_sales["total_sales"].mean()
    total_stores = forecast["store_nbr"].nunique()
    total_families = forecast["family"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Historical Sales",
        f"{total_sales:,.0f}"
    )
    col2.metric(
        "Average Daily Sales",
        f"{average_daily_sales:,.0f}"
    )
    col3.metric(
        "Total Stores",
        f"{total_stores}"
    )
    col4.metric(
        "Product Families",
        f"{total_families}"
    )

    st.subheader("Historical Daily Sales")

    fig = px.line(
        daily_sales,
        x="date",
        y="total_sales",
        title="Daily Retail Sales Trend"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Product Families by Forecast Demand")

    family_demand = (
        forecast.groupby("family", as_index=False)
        .agg(total_forecast=("y_pred", "sum"))
        .sort_values("total_forecast", ascending=False)
        .head(10)
    )

    fig = px.bar(
        family_demand.sort_values("total_forecast"),
        x="total_forecast",
        y="family",
        orientation="h",
        title="Top 10 Product Families"
    )

    fig.update_layout(
        xaxis_title="Forecast Demand",
        yaxis_title="Product Family"
    )

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# 2. SALES FORECAST
# --------------------------------------------------

elif page == "Sales Forecast":

    st.title("Sales Forecast")
    st.write(
        "Explore actual sales and XGBoost predictions "
        "during the validation period."
    )

    col1, col2 = st.columns(2)

    stores = sorted(forecast["store_nbr"].unique())
    families = sorted(forecast["family"].unique())

    selected_store = col1.selectbox(
        "Select Store",
        ["All Stores"] + stores
    )

    selected_family = col2.selectbox(
        "Select Product Family",
        ["All Families"] + families
    )

    filtered = forecast.copy()

    if selected_store != "All Stores":
        filtered = filtered[
            filtered["store_nbr"] == selected_store
        ]

    if selected_family != "All Families":
        filtered = filtered[
            filtered["family"] == selected_family
        ]

    daily = (
        filtered.groupby("date", as_index=False)
        .agg(
            actual_sales=("sales", "sum"),
            predicted_sales=("y_pred", "sum")
        )
    )

    fig = px.line(
        daily,
        x="date",
        y=["actual_sales", "predicted_sales"],
        markers=True,
        title="Actual vs Predicted Sales"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        legend_title="Sales Type",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Forecast Data")

    st.dataframe(
        daily,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Forecast Results",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="forecast_results.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# 3. MODEL PERFORMANCE
# --------------------------------------------------

elif page == "Model Performance":

    st.title("Model Performance")
    st.write(
        "Comparison of forecasting models using "
        "MAE, RMSE, and WAPE."
    )

    st.subheader("Model Comparison")

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    metric_options = ["MAE", "RMSE", "WAPE (%)"]

    selected_metric = st.selectbox(
        "Select Evaluation Metric",
        metric_options
    )

    fig = px.bar(
        comparison,
        x="Model",
        y=selected_metric,
        color="Model",
        title=f"Model Comparison - {selected_metric}"
    )

    fig.update_layout(
        xaxis_title="Forecasting Model",
        yaxis_title=selected_metric,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    best_model = comparison.loc[
        comparison[selected_metric].idxmin()
    ]

    st.success(
        f"Best model based on {selected_metric}: "
        f"{best_model['Model']} "
        f"({best_model[selected_metric]:.2f})"
    )

    st.caption(
        "Lower values indicate better performance "
        "for all three evaluation metrics."
    )


# --------------------------------------------------
# 4. INVENTORY PLANNING
# --------------------------------------------------

elif page == "Inventory Planning":

    st.title("Inventory Planning")
    st.write(
        "Scenario-based inventory planning using "
        "XGBoost forecast demand."
    )

    st.info(
        "This page presents a simulation based on assumed "
        "inventory parameters, not actual stock records."
    )

    col1, col2 = st.columns(2)

    stores = sorted(inventory["store_nbr"].unique())
    families = sorted(inventory["family"].unique())

    selected_store = col1.selectbox(
        "Select Store",
        ["All Stores"] + stores,
        key="inventory_store"
    )

    selected_family = col2.selectbox(
        "Select Product Family",
        ["All Families"] + families,
        key="inventory_family"
    )

    filtered_inventory = inventory.copy()

    if selected_store != "All Stores":
        filtered_inventory = filtered_inventory[
            filtered_inventory["store_nbr"] == selected_store
        ]

    if selected_family != "All Families":
        filtered_inventory = filtered_inventory[
            filtered_inventory["family"] == selected_family
        ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Forecast Demand",
        f"{filtered_inventory['total_forecast_demand'].sum():,.0f}"
    )

    col2.metric(
        "Total Safety Stock",
        f"{filtered_inventory['safety_stock'].sum():,.0f}"
    )

    col3.metric(
        "Total Reorder Point",
        f"{filtered_inventory['reorder_point'].sum():,.0f}"
    )

    st.subheader("Inventory Planning Table")

    display_columns = [
        "store_nbr",
        "family",
        "avg_daily_demand",
        "lead_time_demand",
        "safety_stock",
        "reorder_point",
        "target_stock_level"
    ]

    st.dataframe(
        filtered_inventory[display_columns],
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Inventory Plan",
        data=filtered_inventory.to_csv(index=False).encode("utf-8"),
        file_name="inventory_plan.csv",
        mime="text/csv"
    )

    st.subheader("Top 10 Store-Product Combinations by Reorder Point")

    top_inventory = (
        filtered_inventory.nlargest(10, "reorder_point")
        .copy()
    )

    top_inventory["store_family"] = (
        "Store "
        + top_inventory["store_nbr"].astype(str)
        + " - "
        + top_inventory["family"]
    )

    fig = px.bar(
        top_inventory.sort_values("reorder_point"),
        x="reorder_point",
        y="store_family",
        orientation="h",
        title="Top 10 Reorder Points"
    )

    fig.update_layout(
        xaxis_title="Reorder Point",
        yaxis_title="Store - Product Family"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Simulation assumptions: 3-day lead time, "
        "20% safety stock of lead-time demand, "
        "and 1-day review period."
    )
