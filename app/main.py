from fastapi import FastAPI
import ast
import pandas as pd
import math
from app.schemas import InsightResponse
from app.service import load_insights
from app.service import load_kpis

app = FastAPI(
    title="Business Decision Intelligence Engine",
    description="API for KPI anomaly detection, root-cause analysis, forecasting, and decision insights",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/insights")
def get_insights():
    df = pd.read_csv("data/kpi/decision_insights.csv")

    def safe_parse(value):
        # Handle NaN
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return None

        # Convert stringified lists/dicts safely
        if isinstance(value, str):
            try:
                parsed = ast.literal_eval(value)
                return parsed
            except Exception:
                return value

        # Convert numpy types
        try:
            return value.item()
        except Exception:
            return value

    # Apply parsing column-wise
    for col in df.columns:
        df[col] = df[col].apply(safe_parse)

    # Convert to list of dicts (JSON-safe)
    records = df.to_dict(orient="records")

    return records

@app.get("/kpis")
def get_kpis():
    return load_kpis()
