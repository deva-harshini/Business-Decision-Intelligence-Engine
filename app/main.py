from fastapi import FastAPI
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

@app.get("/insights", response_model=InsightResponse)
def get_decision_insights():
    insights = load_insights()
    return {"insights": insights}
@app.get("/kpis")
def get_kpis():
    return load_kpis()
