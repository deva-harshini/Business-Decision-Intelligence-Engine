import pandas as pd

def forecast_kpi(
    df,
    value_col,
    window=7,
    horizon=14
):
    df = df.sort_values("date").copy()

    rolling_mean = df[value_col].rolling(window).mean().iloc[-1]
    rolling_std = df[value_col].rolling(window).std().iloc[-1]

    future_dates = pd.date_range(
        start=df["date"].iloc[-1] + pd.Timedelta(days=1),
        periods=horizon
    )

    forecast = pd.DataFrame({
        "date": future_dates,
        "forecast": rolling_mean,
        "upper": rolling_mean + 2 * rolling_std,
        "lower": rolling_mean - 2 * rolling_std
    })

    return forecast
