"""
Production Pipeline Script
Business Decision Intelligence Engine
Runs end-to-end KPI → Anomaly → Forecast → Insight workflow
"""

# ============================================================
# PATH SETUP (CRITICAL – DO NOT REMOVE)
# ============================================================
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ============================================================
# STANDARD IMPORTS
# ============================================================
import pandas as pd
from datetime import datetime

# ============================================================
# PROJECT IMPORTS
# ============================================================
from src.kpi_calculator import compute_daily_kpis
from src.anomaly_detector import detect_anomalies
from src.forecasting import forecast_kpi
from src.insight_engine import (
    classify_risk,
    generate_insight,
    compute_confidence,
    generate_validity_date
)

# ============================================================
# CONFIGURATION
# ============================================================
RAW_DATA_PATH = "data/raw/online_retail.csv"
CLEAN_DATA_PATH = "data/processed/cleaned_transactions.csv"

KPI_DIR = "data/kpi"
KPI_PATH = f"{KPI_DIR}/daily_kpis.csv"
INCIDENT_PATH = f"{KPI_DIR}/revenue_incidents.csv"
FORECAST_PATH = f"{KPI_DIR}/revenue_forecast.csv"
INSIGHTS_PATH = f"{KPI_DIR}/decision_insights.csv"

WINDOW = 7
Z_THRESHOLD = 2
FORECAST_DAYS = 14

# ============================================================
# UTILS
# ============================================================
def ensure_directories():
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs(KPI_DIR, exist_ok=True)

# ============================================================
# PIPELINE
# ============================================================
def main():
    print("🚀 Starting Business Decision Intelligence Pipeline")
    print(f"🕒 Run time: {datetime.now().isoformat()}")

    ensure_directories()

    # --------------------------------------------------------
    # 1. LOAD RAW DATA
    # --------------------------------------------------------
    print("📥 Loading raw data...")
    df = pd.read_csv(RAW_DATA_PATH, encoding="ISO-8859-1")

    # --------------------------------------------------------
    # 2. CLEAN DATA
    # --------------------------------------------------------
    print("🧹 Cleaning data...")
    df = df.dropna(subset=["CustomerID"])
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["date"] = df["InvoiceDate"].dt.date
    df["date"] = pd.to_datetime(df["date"])

    df.to_csv(CLEAN_DATA_PATH, index=False)

    # --------------------------------------------------------
    # 3. COMPUTE KPIs
    # --------------------------------------------------------
    print("📊 Computing daily KPIs...")
    daily_kpis = compute_daily_kpis(df)
    daily_kpis.to_csv(KPI_PATH, index=False)

    # --------------------------------------------------------
    # 4. ANOMALY DETECTION
    # --------------------------------------------------------
    print("🚨 Detecting revenue anomalies...")
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

    # --------------------------------------------------------
    # 5. FORECASTING
    # --------------------------------------------------------
    print("📈 Forecasting revenue risk...")
    forecast_df = forecast_kpi(
        daily_kpis,
        value_col="revenue",
        horizon=FORECAST_DAYS
    )

    forecast_df.to_csv(FORECAST_PATH, index=False)

    # --------------------------------------------------------
    # 6. DECISION INSIGHTS (CONFIDENCE + AUDIT)
    # --------------------------------------------------------
    print("🧠 Generating decision insights with confidence & audit trail...")

    baseline = daily_kpis["revenue"].mean()
    volatility = daily_kpis["revenue"].std()

    insights = []

    for _, row in incidents.iterrows():
        future_risk = forecast_df["lower"].min() < baseline * 0.9

        confidence = compute_confidence(
            z_score=row["revenue_zscore"],
            volatility=volatility
        )

        insights.append({
            "date": row["date"],
            "risk_level": classify_risk(row["revenue_zscore"], future_risk),
            "confidence_score": confidence,
            "valid_until": generate_validity_date(row["date"]),
            "insight": generate_insight(row, baseline),
            "audit": {
                "baseline_revenue": round(baseline, 2),
                "z_score": round(row["revenue_zscore"], 2),
                "rolling_window_days": WINDOW,
                "forecast_horizon_days": FORECAST_DAYS
            },
            "generated_at": datetime.now().isoformat()
        })

    insights_df = pd.DataFrame(insights)
    insights_df.to_csv(INSIGHTS_PATH, index=False)

    print("✅ Pipeline completed successfully")
    print(f"📄 Insights written to: {INSIGHTS_PATH}")

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    main()
