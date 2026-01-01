import pandas as pd

def compute_daily_kpis(df):
    daily_kpis = (
        df.groupby("date")
        .agg(
            revenue=("Revenue", "sum"),
            orders=("InvoiceNo", "nunique"),
            customers=("CustomerID", "nunique"),
            quantity=("Quantity", "sum")
        )
        .reset_index()
    )
    daily_kpis["aov"] = daily_kpis["revenue"] / daily_kpis["orders"]
    return daily_kpis
