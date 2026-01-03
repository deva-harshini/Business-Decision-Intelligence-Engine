def classify_risk(z_score, forecast_risk):
    if abs(z_score) > 3 or forecast_risk:
        return "HIGH"
    elif abs(z_score) > 2:
        return "MEDIUM"
    else:
        return "LOW"


def generate_insight(row, baseline):
    direction = "decrease" if row["revenue_zscore"] < 0 else "increase"

    insight = (
        f"Revenue showed an abnormal {direction} on {row['date'].date()} "
        f"with a z-score of {row['revenue_zscore']:.2f}. "
    )

    if row["revenue"] < baseline:
        insight += "Revenue fell below historical baseline levels. "

    return insight
