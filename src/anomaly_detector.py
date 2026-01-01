import pandas as pd

def detect_anomalies(
    df,
    value_col,
    window=7,
    z_threshold=2
):
    df = df.copy()

    mean_col = f"{value_col}_mean"
    std_col = f"{value_col}_std"
    z_col = f"{value_col}_zscore"
    flag_col = f"{value_col}_anomaly"

    df[mean_col] = (
        df[value_col]
        .rolling(window, min_periods=window)
        .mean()
    )

    df[std_col] = (
        df[value_col]
        .rolling(window, min_periods=window)
        .std()
    )

    df[z_col] = (df[value_col] - df[mean_col]) / df[std_col]
    df[flag_col] = df[z_col].abs() > z_threshold

    return df
