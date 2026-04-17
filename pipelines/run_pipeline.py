"""
Production Pipeline Script
Business Decision Intelligence Engine
"""

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
from datetime import datetime

from src.kpi_calculator import compute_daily_kpis
from src.anomaly_detector import detect_anomalies
from src.forecasting import forecast_kpi
from src.insight_engine import (
    classify_risk,
    generate_insight,
    compute_confidence,
    generate_validity_date,
    generate_business_insights
)
from src.action_engine import recommend_actions

RAW_DATA_PATH = "data/raw/online_retail.csv"
CLEAN_DATA_PATH = "data/processed/cleaned_transactions.csv"

KPI_DIR = "data/kpi"
KPI_PATH = f"{KPI_DIR}/daily_kpis.csv"
INSIGHTS_PATH = f"{KPI_DIR}/decision_insights.csv"

WINDOW = 7
Z_THRESHOLD = 2
FORECAST_DAYS = 14


def ensure_directories():
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs(KPI_DIR, exist_ok=True)


def main():
    print("🚀 Running pipeline...")

    ensure_directories()

    # Load data
    df = pd.read_csv(RAW_DATA_PATH, encoding="ISO-8859-1")

    df = df.dropna(subset=["CustomerID"])
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["date"] = pd.to_datetime(df["InvoiceDate"].dt.date)

    df.to_csv(CLEAN_DATA_PATH, index=False)

    # KPIs
    daily_kpis = compute_daily_kpis(df)
    daily_kpis.to_csv(KPI_PATH, index=False)

    # Anomalies
    daily_kpis = detect_anomalies(
        daily_kpis,
        value_col="revenue",
        window=WINDOW,
        z_threshold=Z_THRESHOLD
    )

    # Forecast
    forecast_df = forecast_kpi(
        daily_kpis,
        value_col="revenue",
        horizon=FORECAST_DAYS
    )

    baseline = float(daily_kpis["revenue"].mean())
    volatility = float(daily_kpis["revenue"].std())

    global_insights = generate_business_insights(daily_kpis)

    insights = []

    # 🔥 FIX: iterate over ALL rows (not just anomalies)
    for _, row in daily_kpis.iterrows():

        z_score = float(row.get("revenue_zscore", 0))
        future_risk = forecast_df["lower"].min() < baseline * 0.9

        risk_level = classify_risk(z_score, future_risk)

        confidence = compute_confidence(
            z_score=z_score,
            volatility=volatility
        )

        actions = recommend_actions(
            risk_level=risk_level,
            z_score=z_score,
            forecast_risk=future_risk,
            insights=global_insights
        )

        insights.append({
            "date": row["date"],
            "risk_level": risk_level,
            "confidence_score": confidence,
            "valid_until": generate_validity_date(row["date"]),
            "insight": generate_insight(row, baseline),
            "recommended_actions": actions,
            "audit": {
                "baseline_revenue": round(baseline, 2),
                "z_score": round(z_score, 2)
            },
            "generated_at": datetime.now().isoformat()
        })

    insights_df = pd.DataFrame(insights)
    insights_df.to_csv(INSIGHTS_PATH, index=False)

    print("✅ Pipeline completed")


if __name__ == "__main__":
    main()