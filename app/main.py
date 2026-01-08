from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

# =====================================================
# APP INITIALIZATION
# =====================================================
app = FastAPI(
    title="Business Decision Intelligence API",
    description="API serving KPI risk insights, confidence scores, audit trail, and business action recommendations",
    version="1.0.0"
)

# =====================================================
# CORS (for Streamlit / external clients)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# PATH CONFIG
# =====================================================
INSIGHTS_PATH = "data/kpi/decision_insights.csv"

# =====================================================
# HEALTH CHECK
# =====================================================
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Business Decision Intelligence API is running"}

# =====================================================
# LOAD INSIGHTS SAFELY
# =====================================================
def load_insights():
    if not os.path.exists(INSIGHTS_PATH):
        raise FileNotFoundError(
            "decision_insights.csv not found. Run pipeline before starting API."
        )

    df = pd.read_csv(INSIGHTS_PATH)

    # Convert stringified JSON columns safely
    if "audit" in df.columns:
        df["audit"] = df["audit"].apply(
            lambda x: eval(x) if isinstance(x, str) else x
        )

    if "recommended_actions" in df.columns:
        df["recommended_actions"] = df["recommended_actions"].apply(
            lambda x: eval(x) if isinstance(x, str) else x
        )

    return df

# =====================================================
# GET INSIGHTS
# =====================================================
@app.get("/insights")
def get_insights(risk_level: str | None = None):
    """
    Fetch decision insights.
    Optional filter: risk_level = HIGH / MEDIUM / LOW
    """
    try:
        df = load_insights()

        if risk_level:
            df = df[df["risk_level"] == risk_level.upper()]

        return {
            "count": len(df),
            "insights": df.to_dict(orient="records")
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error loading insights: {str(e)}"
        )

# =====================================================
# ROOT
# =====================================================
@app.get("/")
def root():
    return {
        "message": "Welcome to the Business Decision Intelligence API",
        "docs": "/docs",
        "health": "/health",
        "insights": "/insights"
    }
@app.get("/kpis")
def get_kpis():
    df = load_insights()
    return df[["date", "risk_level", "confidence_score"]].to_dict(orient="records")
