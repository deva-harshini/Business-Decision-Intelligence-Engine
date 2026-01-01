import pandas as pd

def attribute_revenue_change(
    before_df,
    after_df,
    group_col="StockCode"
):
    before = (
        before_df.groupby(group_col)["Revenue"]
        .sum()
        .reset_index(name="before")
    )

    after = (
        after_df.groupby(group_col)["Revenue"]
        .sum()
        .reset_index(name="after")
    )

    contrib = before.merge(
        after,
        on=group_col,
        how="outer"
    ).fillna(0)

    contrib["change"] = contrib["after"] - contrib["before"]

    return contrib.sort_values("change")
