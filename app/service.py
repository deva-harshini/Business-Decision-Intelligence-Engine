import pandas as pd

DATA_PATH = "data/kpi/decision_insights.csv"

def load_insights():
    df = pd.read_csv(DATA_PATH)
    return df.to_dict(orient="records")
