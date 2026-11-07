def create_features(df):

    df = df.sort_values(
        ["County", "Year"]
    )

    df["Growth_Rate"] = (
        df.groupby("County")
        ["Production_Tonnes"]
        .pct_change()
    )

    df["Growth_Rate"] = df["Growth_Rate"].fillna(0)

    df["Rolling_Mean"] = (
        df.groupby("County")
        ["Production_Tonnes"]
        .transform(
            lambda x: x.rolling(
                window=3,
                min_periods=1
            ).mean()
        )
    )

    return df