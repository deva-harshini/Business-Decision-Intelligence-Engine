from pydantic import BaseModel
from typing import List

class Insight(BaseModel):
    date: str
    risk_level: str
    insight: str


class InsightResponse(BaseModel):
    insights: List[Insight]
