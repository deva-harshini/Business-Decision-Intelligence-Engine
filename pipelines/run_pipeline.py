"""
Production Pipeline Script
Runs end-to-end Business Decision Intelligence workflow
"""

import sys
import os
import pandas as pd
from datetime import datetime

# -----------------------------
# PATH SETUP (IMPORTANT)
# -----------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# -----------------------------
# IMPORT CORE LOGIC
# -----------------------------
from src.kpi_calculator import compute_daily_kpis
from src.anomaly_detector import detect_anomalies
from src.forecasting import forecast_kpi
from src.insight_engine import classify_risk, generate_insight

# -----------------------------
# CONFIG
# -----------------------------
RAW_DATA_PATH = "data/raw/online_retail.csv"
CLEAN_DATA_PATH = "data/processed/cleaned_transactions.csv"
KPI_PATH = "data/kpi/daily_kpis.csv"
INCIDENT_PATH = "data/kpi/revenue_incidents.csv"
FORECAST_PATH = "data/kpi/revenue_forecast.csv"
INSIGHTS_PATH = "data/kpi/decision_insights.csv"

WINDOW = 7
Z_THRESHOLD = 2
FORECAST_DAYS = 14

# -----------------------------
# PIPELINE START
# -----------------------------
def main():
    print("🚀 Starting Business Decision Intelligence Pipeline")
    print(f"🕒 Run time: {datetime.now()}")

    # 1. Load Raw Data
    print("📥 Loading raw data...")
    df = pd.read_csv(RAW_DATA_PATH, encoding="ISO-8859-1")

    # 2. Clean Data
    print("🧹 Cleaning data...")
    df = df.dropna(subset=["CustomerID"])
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["date"] = df["InvoiceDate"].dt.date
    df["date"] = pd.to_datetime(df["date"])

    df.to_csv(CLEAN_DATA_PATH, index=False)

    # 3. Compute KPIs
    print("📊 Computing daily KPIs...")
    daily_kpis = compute_daily_kpis(df)
    daily_kpis.to_csv(KPI_PATH, index=False)

    # 4. Detect Anomalies
    print("🚨 Detecting KPI anomalies...")
    daily_kpis = detect_anomalies(
        daily_kpis,
        value_col="revenue",
        window=WINDOW,
        z_threshold=Z_THRESHOLD
    )

    incidents = daily_kpis[daily_kpis["revenue_anomaly"]][
        ["date", "revenue", "revenue_zscore"]
    ].copy()

    incidents.to_csv(INCIDENT_PATH, index=False)

    # 5. Forecast KPIs
    print("📈 Forecasting future KPI risk...")
    forecast_df = forecast_kpi(
        daily_kpis,
        value_col="revenue",
        horizon=FORECAST_DAYS
    )

    forecast_df.to_csv(FORECAST_PATH, index=False)

    # 6. Generate Decision Insights
    print("🧠 Generating decision insights...")
    baseline = daily_kpis["revenue"].mean()
    insights = []

    for _, row in incidents.iterrows():
        future_risk = forecast_df["lower"].min() < baseline * 0.9

        insights.append({
            "date": row["date"],
            "risk_level": classify_risk(row["revenue_zscore"], future_risk),
            "insight": generate_insight(row, baseline),
            "generated_at": datetime.now().isoformat()
        })

    insights_df = pd.DataFrame(insights)
    insights_df.to_csv(INSIGHTS_PATH, index=False)

    print("✅ Pipeline completed successfully")
    print(f"📄 Insights saved to {INSIGHTS_PATH}")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()
