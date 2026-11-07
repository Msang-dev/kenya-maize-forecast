import pandas as pd


def load_data(filepath):

    df = pd.read_excel(
        filepath,
        sheet_name="Sheet4"
    )

    return df


def reshape_data(df):

    pivot = (
        df.pivot_table(
            index=["County", "Year"],
            columns="Indicator",
            values="Value",
            aggfunc="first"
        )
        .reset_index()
    )

    pivot.columns.name = None

    pivot = pivot.rename(
        columns={
            "Area (HA)": "Area_Hectares",
            "Production (MT)": "Production_Tonnes",
            "Yield(MT/HA)": "Yield"
        }
    )

    pivot["County"] = pivot["County"].astype(str).str.strip()

    return pivot