# Retail Sales Forecasting & Inventory Planning

A machine learning project that forecasts retail sales across multiple stores and product families using historical sales data. The project also translates demand forecasts into inventory planning insights through a scenario-based inventory simulation.

## Project Overview

Accurate sales forecasting helps retailers anticipate customer demand and make better inventory planning decisions. This project uses historical retail sales data from Corporación Favorita to develop and evaluate machine learning models for daily sales forecasting.

The best-performing model is then used to support an inventory planning simulation by estimating lead-time demand, safety stock, reorder points, and target stock levels.

## Objectives

- Analyze historical retail sales patterns across stores and product families.
- Develop and compare multiple time series forecasting approaches.
- Identify the best-performing forecasting model using evaluation metrics.
- Translate forecasted demand into inventory planning indicators.
- Present analytical results through an interactive Streamlit dashboard.

## Dataset

**Source:** [Store Sales - Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting/data)

The dataset contains historical retail sales and supporting information from Corporación Favorita, Ecuador.

Key data sources include:

| Dataset | Description |
|---|---|
| Train | Historical daily sales by store and product family |
| Stores | Store location, type, and cluster information |
| Oil | Daily oil prices |
| Holidays | Holiday and event information |
| Transactions | Daily store transaction records |

The analysis covers 54 stores and 33 product families, with historical sales data from January 2013 to August 2017.

## Methodology

The project follows these stages:

1. **Data Understanding & EDA** – Explore sales trends, distributions, product families, and store characteristics.
2. **Data Preprocessing** – Handle missing values, validate records, and integrate supporting datasets.
3. **Feature Engineering** – Generate calendar features, lag features, and rolling statistics.
4. **Modeling** – Train and evaluate three forecasting approaches:
   - Seasonal Naive (7-day lag)
   - Random Forest Regressor
   - XGBoost Regressor
5. **Model Evaluation** – Compare model performance using MAE, RMSE, and WAPE.
6. **Inventory Planning Simulation** – Calculate lead-time demand, safety stock, reorder points, and target stock levels.
7. **Dashboard Development** – Build an interactive dashboard using Streamlit.

## Model Performance

The models were evaluated on a 16-day validation period from July 31 to August 15, 2017.

| Model | MAE | RMSE | WAPE |
|---|---:|---:|---:|
| Seasonal Naive | 96.54 | 348.38 | 20.67% |
| Random Forest | 79.17 | 270.49 | 16.95% |
| **XGBoost** | **69.41** | **235.20** | **14.86%** |

XGBoost achieved the best performance across all three evaluation metrics and was selected for the inventory planning simulation.

## Inventory Planning Simulation

Forecasted demand is translated into inventory planning indicators using the following assumptions:

| Parameter | Value |
|---|---:|
| Forecasting Model | XGBoost |
| Lead Time | 3 days |
| Review Period | 1 day |
| Safety Stock | 20% of Lead-Time Demand |

The simulation provides:
- Average daily demand
- Lead-time demand
- Safety stock
- Reorder point (ROP)
- Target stock level

**Note:** The dataset does not include actual inventory levels or supplier lead-time records. Therefore, the inventory planning component represents a scenario-based simulation rather than actual inventory optimization.

## Streamlit Dashboard

The interactive dashboard consists of four main pages:

1. **Executive Overview** – Historical sales trends and key business metrics.
2. **Sales Forecast** – Actual versus predicted sales with store and product family filters.
3. **Model Performance** – Comparison of forecasting models.
4. **Inventory Planning** – Simulated inventory indicators and replenishment prioritization.

**Live Dashboard:** [Insert Streamlit URL after deployment]

## Tech Stack

- **Programming Language:** Python
- **Data Analysis:** Pandas, NumPy
- **Machine Learning:** Scikit-learn, XGBoost
- **Data Visualization:** Matplotlib, Plotly
- **Dashboard:** Streamlit
- **Development Environment:** Google Colab, Visual Studio Code
- **Version Control:** Git, GitHub

## Project Structure

```text
retail-sales-forecasting/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── retail_sales_forecasting.ipynb
├── dashboard/
│   └── app.py
├── models/
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation & Usage

Clone this repository:

```bash
git clone https://github.com/USERNAME/retail-sales-forecasting.git
cd retail-sales-forecasting
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

Make sure the processed CSV files are available in the `data/processed/` directory before running the dashboard.

## Limitations

- Model performance is evaluated on a single 16-day validation period.
- Random Forest and XGBoost were trained using a 300,000-row sample due to computational constraints.
- Actual inventory and stockout data are unavailable.
- Inventory parameters are based on assumptions rather than operational records.
- External demand factors may not be fully represented in the dataset.

## Acknowledgements

Dataset provided by Corporación Favorita through the Kaggle Store Sales - Time Series Forecasting competition.