from pydantic import BaseModel
from typing import Dict, List
from typing import List, Dict

class Insight(BaseModel):
    date: str
    risk_level: str
    confidence_score: float
    valid_until: str
    insight: str
    recommended_actions: List[Dict]
    audit: Dict
    generated_at: str

class InsightResponse(BaseModel):
    insights: List[Insight]
