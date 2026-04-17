from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import ast
import tempfile
import traceback


app = FastAPI(
    title="Business Decision Intelligence API",
    version="2.1.0"
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
        "endpoints": ["/insights", "/kpis", "/health", "/upload"]
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


# -----------------------------
# 🔥 UPLOAD DATASET (FIXED)
# -----------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save temp file
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(await file.read())
        temp.close()

        df = pd.read_csv(temp.name)

        # -----------------------------
        # SAFE DATE DETECTION
        # -----------------------------
        date_col = None

        for col in df.columns:
            if "date" in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_col = col
                    break
                except:
                    continue

        if date_col is None:
            return {"error": "No valid date column found (column should contain 'date')"}

        df["date"] = df[date_col]

        # -----------------------------
        # SAFE REVENUE CREATION
        # -----------------------------
        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) == 0:
            return {"error": "No numeric columns found in dataset"}

        if "revenue" not in df.columns:
            df["revenue"] = df[numeric_cols].sum(axis=1)
        
        if "sales" not in df.columns:
            df["sales"] = df["revenue"]
            
        if "profit" not in df.columns:
            df["profit"] = df["revenue"] * 0.2 

        # -----------------------------
        # PIPELINE
        # -----------------------------
        from src.kpi_calculator import compute_daily_kpis
        from src.anomaly_detector import detect_anomalies
        from src.insight_engine import generate_business_insights

        kpis = compute_daily_kpis(df)
        kpis = detect_anomalies(kpis, "revenue")

        insights = generate_business_insights(kpis)

        return {
            "kpis": kpis.head(20).to_dict(orient="records"),
            "insights": insights
        }

    except Exception as e:
        return {
            "error": str(e),
            "trace": traceback.format_exc()}