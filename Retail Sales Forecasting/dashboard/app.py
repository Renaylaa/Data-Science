from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Retail Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Project paths
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "Data" / "processed"

# --------------------------------------------------
# DESIGN TOKENS
# --------------------------------------------------

NAVY = "#14263A"
INK = "#1F2D3D"
TEXT_MUTED = "#6B7A74"
TEXT_SOFT = "#93A09A"
GREEN = "#2F8F6B"
GREEN_DARK = "#256F54"
MUTED_GREEN = "#A9CBBC"
LIGHT_GREEN = "#E7F2EC"
BORDER = "#E6EAE8"
BG = "#F5F7F6"
SURFACE = "#FFFFFF"

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], [data-testid="stApp"],
button, input, select, textarea {{
    font-family: 'Poppins', sans-serif !important;
}}

.stApp {{
    background-color: {BG};
    color: {INK};
}}

#MainMenu, footer {{
    visibility: hidden;
}}

[data-testid="stHeader"] {{
    background-color: transparent;
}}

.block-container {{
    padding: 2.2rem 3rem 3rem 3rem;
    max-width: 1500px;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: {SURFACE};
    border-right: 1px solid {BORDER};
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1rem;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] > label {{
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 1.4px;
    color: {TEXT_SOFT};
    text-transform: uppercase;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {{
    gap: 4px;
    margin-top: 8px;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {{
    padding: 9px 12px;
    border-radius: 8px;
    width: 100%;
    transition: background-color 0.15s ease;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover {{
    background-color: {BG};
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label p {{
    font-size: 13px;
    font-weight: 500;
    color: {INK};
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {{
    background-color: {LIGHT_GREEN};
}}

[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p {{
    color: {GREEN_DARK};
    font-weight: 600;
}}

/* Typography */
h1, h2, h3 {{
    color: {NAVY};
    letter-spacing: -0.01em;
}}

h3 {{
    font-size: 16px !important;
    font-weight: 600 !important;
    margin-bottom: 0.4rem;
}}

p {{
    font-size: 13px;
}}

/* Metric cards */
[data-testid="stMetric"] {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 1px 2px rgba(20, 38, 58, 0.03);
    border-top: 3px solid {GREEN};
}}

[data-testid="stMetricLabel"] p {{
    color: {TEXT_MUTED};
    font-size: 12px;
    font-weight: 500;
}}

[data-testid="stMetricValue"] {{
    color: {NAVY};
    font-weight: 600;
    font-size: 26px;
}}

/* Charts and tables */
[data-testid="stPlotlyChart"] {{
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 14px 14px 6px 14px;
    box-shadow: 0 1px 2px rgba(20, 38, 58, 0.03);
}}

[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 12px;
    overflow: hidden;
}}

/* Inputs */
.stSelectbox label p, .stRadio label p {{
    color: #40544A;
    font-weight: 500;
    font-size: 12.5px;
}}

[data-baseweb="select"] > div {{
    border-radius: 10px;
    border-color: {BORDER};
    background-color: {SURFACE};
}}

/* Buttons */
.stButton button, .stDownloadButton button {{
    background-color: {GREEN};
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 500;
    font-size: 13px;
    padding: 8px 20px;
    transition: background-color 0.15s ease;
}}

.stButton button:hover, .stDownloadButton button:hover {{
    background-color: {GREEN_DARK};
    color: white;
    border: none;
}}

hr {{
    border-color: {BORDER};
    margin: 1.1rem 0;
}}

[data-testid="stAlert"] {{
    border-radius: 12px;
    border: 1px solid {BORDER};
}}

[data-testid="stCaptionContainer"] {{
    color: {TEXT_SOFT};
}}

/* Reusable blocks */
.page-eyebrow {{
    font-size: 11px;
    color: {GREEN};
    font-weight: 600;
    letter-spacing: 1.6px;
    margin-bottom: 8px;
}}

.page-title {{
    font-size: 28px;
    color: {NAVY};
    font-weight: 600;
    line-height: 1.25;
    letter-spacing: -0.02em;
}}

.page-desc {{
    font-size: 13px;
    color: {TEXT_MUTED};
    margin-top: 6px;
}}

.section-gap {{
    height: 22px;
}}

.best-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-left: 4px solid {GREEN};
    border-radius: 12px;
    padding: 18px 22px;
    margin-top: 14px;
}}

.best-card .label {{
    font-size: 10.5px;
    color: {GREEN};
    font-weight: 600;
    letter-spacing: 1.4px;
}}

.best-card .name {{
    font-size: 19px;
    color: {NAVY};
    font-weight: 600;
    margin-top: 6px;
}}

.best-card .value {{
    font-size: 13px;
    color: {TEXT_MUTED};
    margin-top: 3px;
}}
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# PLOTLY THEME
# --------------------------------------------------

def style_chart(fig, height=380):
    fig.update_layout(
        template="plotly_white",
        height=height,
        font=dict(family="Poppins", size=11, color=INK),
        title=None,
        margin=dict(l=16, r=16, t=24, b=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor=BORDER,
            font_family="Poppins",
            font_size=12,
            font_color=INK,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11, color=TEXT_MUTED),
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor=BORDER,
            tickfont=dict(color=TEXT_MUTED),
            title_font=dict(color=TEXT_MUTED, size=11),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#EEF1EF",
            zeroline=False,
            tickfont=dict(color=TEXT_MUTED),
            title_font=dict(color=TEXT_MUTED, size=11),
        ),
    )
    return fig


def gap():
    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    daily_sales = pd.read_csv(DATA_DIR / "daily_sales.csv", parse_dates=["date"])
    forecast = pd.read_csv(DATA_DIR / "forecast_results.csv", parse_dates=["date"])
    comparison = pd.read_csv(DATA_DIR / "model_comparison.csv")
    inventory = pd.read_csv(DATA_DIR / "inventory_plan.csv")
    return daily_sales, forecast, comparison, inventory


try:
    daily_sales, forecast, comparison, inventory = load_data()

except FileNotFoundError as e:
    st.error(f"Data file not found: {e}")
    st.info("Please check the processed data folder.")
    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        f"""
        <div style="padding: 10px 0 6px 0;">
            <div style="font-size:11px; color:{GREEN};
                        font-weight:600; letter-spacing:2px;">
                RETAIL ANALYTICS
            </div>
            <div style="font-size:20px; color:{NAVY};
                        font-weight:600; margin-top:6px;
                        letter-spacing:-0.01em;">
                Sales Intelligence
            </div>
            <div style="font-size:11.5px; color:{TEXT_SOFT};
                        margin-top:4px;">
                Forecasting and Inventory Planning
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Executive Overview",
            "Sales Forecast",
            "Model Performance",
            "Inventory Planning",
        ],
    )

    st.divider()

    st.markdown(
        f"""
        <div style="font-size:10.5px; color:{TEXT_SOFT};
                    font-weight:600; letter-spacing:1.4px;">
            FORECASTING ENGINE
        </div>
        <div style="font-size:13px; color:{NAVY};
                    font-weight:500; margin-top:5px;">
            XGBoost Regressor
        </div>
        <div style="font-size:11px; color:{TEXT_SOFT};
                    margin-top:22px; line-height:1.6;">
            Retail Sales Forecasting<br>
            Data Science Portfolio
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

def page_header(title, description):
    st.markdown(
        f"""
        <div style="margin-bottom:26px;">
            <div class="page-eyebrow">RETAIL SALES FORECASTING</div>
            <div class="page-title">{title}</div>
            <div class="page-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# 1. EXECUTIVE OVERVIEW
# --------------------------------------------------

if page == "Executive Overview":

    page_header(
        "Executive Overview",
        "An overview of historical retail performance and forecasted demand.",
    )

    total_sales = daily_sales["total_sales"].sum()
    average_daily_sales = daily_sales["total_sales"].mean()
    total_stores = forecast["store_nbr"].nunique()
    total_families = forecast["family"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Historical Sales", f"{total_sales:,.0f}")
    col2.metric("Average Daily Sales", f"{average_daily_sales:,.0f}")
    col3.metric("Total Stores", f"{total_stores:,}")
    col4.metric("Product Families", f"{total_families:,}")

    gap()

    st.subheader("Historical Sales Trend")

    fig = px.line(
        daily_sales,
        x="date",
        y="total_sales",
        color_discrete_sequence=[GREEN],
    )

    fig.update_traces(
        line=dict(width=2),
        fill="tozeroy",
        fillcolor="rgba(47, 143, 107, 0.08)",
        hovertemplate="%{x|%d %b %Y}<br>Sales: %{y:,.0f}<extra></extra>",
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Total Sales",
        showlegend=False,
    )

    st.plotly_chart(style_chart(fig, 390), use_container_width=True)

    gap()

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
        color_discrete_sequence=[GREEN],
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate="%{y}<br>Demand: %{x:,.0f}<extra></extra>",
    )

    fig.update_layout(
        xaxis_title="Forecast Demand",
        yaxis_title=None,
        showlegend=False,
        bargap=0.35,
    )

    st.plotly_chart(style_chart(fig, 400), use_container_width=True)

# --------------------------------------------------
# 2. SALES FORECAST
# --------------------------------------------------

elif page == "Sales Forecast":

    page_header(
        "Sales Forecast",
        "Compare actual sales against XGBoost predictions.",
    )

    col1, col2 = st.columns(2)

    stores = sorted(forecast["store_nbr"].unique())
    families = sorted(forecast["family"].unique())

    selected_store = col1.selectbox("Store", ["All Stores"] + stores)
    selected_family = col2.selectbox("Product Family", ["All Families"] + families)

    filtered = forecast.copy()

    if selected_store != "All Stores":
        filtered = filtered[filtered["store_nbr"] == selected_store]

    if selected_family != "All Families":
        filtered = filtered[filtered["family"] == selected_family]

    daily = (
        filtered.groupby("date", as_index=False)
        .agg(
            actual_sales=("sales", "sum"),
            predicted_sales=("y_pred", "sum"),
        )
    )

    actual_total = daily["actual_sales"].sum()
    predicted_total = daily["predicted_sales"].sum()
    difference = predicted_total - actual_total

    gap()

    col1, col2, col3 = st.columns(3)

    col1.metric("Actual Sales", f"{actual_total:,.0f}")
    col2.metric("Predicted Sales", f"{predicted_total:,.0f}")
    col3.metric("Forecast Difference", f"{difference:+,.0f}")

    gap()

    st.subheader("Actual vs Predicted Sales")

    fig = px.line(
        daily,
        x="date",
        y=["actual_sales", "predicted_sales"],
        color_discrete_sequence=[NAVY, GREEN],
        markers=False,
    )

    fig.update_traces(line=dict(width=2.2))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        hovermode="x unified",
        legend_title=None,
    )

    st.plotly_chart(style_chart(fig, 420), use_container_width=True)

    gap()

    st.subheader("Forecast Data")

    st.dataframe(
        daily,
        use_container_width=True,
        hide_index=True,
        column_config={
            "date": st.column_config.DateColumn("Date"),
            "actual_sales": st.column_config.NumberColumn(
                "Actual Sales", format="%.2f"
            ),
            "predicted_sales": st.column_config.NumberColumn(
                "Predicted Sales", format="%.2f"
            ),
        },
    )

    st.download_button(
        "Download Forecast Results",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="forecast_results.csv",
        mime="text/csv",
    )

# --------------------------------------------------
# 3. MODEL PERFORMANCE
# --------------------------------------------------

elif page == "Model Performance":

    page_header(
        "Model Performance",
        "Evaluate and compare forecasting models using error metrics.",
    )

    st.subheader("Model Comparison")

    st.dataframe(comparison, use_container_width=True, hide_index=True)

    gap()

    metric_options = ["MAE", "RMSE", "WAPE (%)"]

    selected_metric = st.selectbox("Evaluation Metric", metric_options)

    best_model = comparison.loc[comparison[selected_metric].idxmin()]

    chart_df = comparison.sort_values(selected_metric).copy()
    chart_df["Status"] = chart_df["Model"].apply(
        lambda m: "Best" if m == best_model["Model"] else "Other"
    )

    fig = px.bar(
        chart_df,
        x="Model",
        y=selected_metric,
        color="Status",
        color_discrete_map={"Best": GREEN, "Other": MUTED_GREEN},
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate="%{x}<br>%{y:,.2f}<extra></extra>",
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=selected_metric,
        showlegend=False,
        bargap=0.45,
    )

    st.plotly_chart(style_chart(fig, 400), use_container_width=True)

    st.markdown(
        f"""
        <div class="best-card">
            <div class="label">BEST PERFORMING MODEL</div>
            <div class="name">{best_model['Model']}</div>
            <div class="value">{selected_metric}: {best_model[selected_metric]:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Lower values indicate better forecasting performance "
        "for all three evaluation metrics."
    )

# --------------------------------------------------
# 4. INVENTORY PLANNING
# --------------------------------------------------

elif page == "Inventory Planning":

    page_header(
        "Inventory Planning",
        "Demand-based inventory planning and replenishment analysis.",
    )

    st.info(
        "This inventory plan is a simulation based on assumed "
        "inventory parameters, not actual stock records."
    )

    col1, col2 = st.columns(2)

    stores = sorted(inventory["store_nbr"].unique())
    families = sorted(inventory["family"].unique())

    selected_store = col1.selectbox(
        "Store", ["All Stores"] + stores, key="inventory_store"
    )

    selected_family = col2.selectbox(
        "Product Family", ["All Families"] + families, key="inventory_family"
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

    gap()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Forecast Demand",
        f"{filtered_inventory['total_forecast_demand'].sum():,.0f}",
    )

    col2.metric(
        "Safety Stock",
        f"{filtered_inventory['safety_stock'].sum():,.0f}",
    )

    col3.metric(
        "Reorder Point",
        f"{filtered_inventory['reorder_point'].sum():,.0f}",
    )

    gap()

    st.subheader("Inventory Planning Table")

    display_columns = [
        "store_nbr",
        "family",
        "avg_daily_demand",
        "lead_time_demand",
        "safety_stock",
        "reorder_point",
        "target_stock_level",
    ]

    st.dataframe(
        filtered_inventory[display_columns],
        use_container_width=True,
        hide_index=True,
        column_config={
            "store_nbr": "Store",
            "family": "Product Family",
            "avg_daily_demand": st.column_config.NumberColumn(
                "Avg. Daily Demand", format="%.2f"
            ),
            "lead_time_demand": st.column_config.NumberColumn(
                "Lead Time Demand", format="%.2f"
            ),
            "safety_stock": st.column_config.NumberColumn(
                "Safety Stock", format="%.2f"
            ),
            "reorder_point": st.column_config.NumberColumn(
                "Reorder Point", format="%.2f"
            ),
            "target_stock_level": st.column_config.NumberColumn(
                "Target Stock Level", format="%.2f"
            ),
        },
    )

    st.download_button(
        "Download Inventory Plan",
        data=filtered_inventory.to_csv(index=False).encode("utf-8"),
        file_name="inventory_plan.csv",
        mime="text/csv",
    )

    gap()

    st.subheader("Top Store-Product Combinations by Reorder Point")

    top_inventory = filtered_inventory.nlargest(10, "reorder_point").copy()

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
        color_discrete_sequence=[GREEN],
    )

    fig.update_traces(marker_line_width=0)

    fig.update_layout(
        xaxis_title="Reorder Point",
        yaxis_title=None,
        showlegend=False,
        bargap=0.35,
    )

    st.plotly_chart(style_chart(fig, 420), use_container_width=True)

    st.caption(
        "Simulation assumptions: 3-day lead time, "
        "20% safety stock of lead-time demand, "
        "and 1-day review period."
    )

#halooooooooo
