from datetime import timedelta

def compute_confidence(z_score, volatility):
    """
    Confidence increases with stronger signal
    Decreases with higher volatility
    """
    base_confidence = min(abs(z_score) / 3, 1.0)
    volatility_penalty = min(volatility / 100000, 0.5)
    confidence = max(base_confidence - volatility_penalty, 0.3)
    return round(confidence, 2)


def classify_risk(z_score, forecast_risk):
    if abs(z_score) > 3 or forecast_risk:
        return "HIGH"
    elif abs(z_score) > 2:
        return "MEDIUM"
    else:
        return "LOW"


def generate_insight(row, baseline):
    direction = "decrease" if row["revenue_zscore"] < 0 else "increase"
    return (
        f"Revenue showed an abnormal {direction} on {row['date'].date()} "
        f"(z-score: {row['revenue_zscore']:.2f}). "
        f"Baseline revenue was {baseline:.0f}."
    )


def generate_validity_date(incident_date, days=2):
    return (incident_date + timedelta(days=days)).date()
