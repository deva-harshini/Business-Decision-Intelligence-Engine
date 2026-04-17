from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import ast

app = FastAPI(
    title="Business Decision Intelligence API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INSIGHTS_PATH = "data/kpi/decision_insights.csv"
KPI_PATH = "data/kpi/daily_kpis.csv"


# -----------------------------
# SAFE PARSER
# -----------------------------
def safe_parse(x):
    try:
        return ast.literal_eval(x) if isinstance(x, str) else x
    except:
        return x


# -----------------------------
# LOAD INSIGHTS
# -----------------------------
def load_insights():
    if not os.path.exists(INSIGHTS_PATH):
        raise FileNotFoundError("Run pipeline first")

    df = pd.read_csv(INSIGHTS_PATH)

    if "audit" in df.columns:
        df["audit"] = df["audit"].apply(safe_parse)

    if "recommended_actions" in df.columns:
        df["recommended_actions"] = df["recommended_actions"].apply(safe_parse)

    return df


# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "Business Decision Intelligence API",
        "endpoints": ["/insights", "/kpis", "/health"]
    }


# -----------------------------
# HEALTH
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# GET INSIGHTS
# -----------------------------
@app.get("/insights")
def get_insights():
    try:
        df = load_insights()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# GET KPIs
# -----------------------------
@app.get("/kpis")
def get_kpis():
    try:
        if not os.path.exists(KPI_PATH):
            raise FileNotFoundError("Run pipeline first")

        df = pd.read_csv(KPI_PATH)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))