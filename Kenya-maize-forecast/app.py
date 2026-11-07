from pathlib import Path

import pandas as pd
import streamlit as st

from src.county_forecast import build_county_forecasts
from src.data import load_data, reshape_data


DATA_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "Maize-Production-2012-2020-Combined.xlsx"
)

st.set_page_config(
    page_title="Kenya maize production forecast",
    page_icon="🌽",
    layout="wide",
)


@st.cache_data
def load_historical_data():
    return reshape_data(load_data(str(DATA_FILE)))


st.title("Kenya maize production forecast")
st.caption(
    "County estimates are derived only from historical production. "
    "Methods are selected by expanding-window backtesting."
)

historical = load_historical_data()
latest_year = int(historical["Year"].max())
counties = sorted(historical["County"].astype(str).unique().tolist())

with st.form("forecast_controls"):
    year_col, county_col = st.columns(2)
    with year_col:
        target_year = st.number_input(
            "Forecast year",
            min_value=latest_year + 1,
            max_value=latest_year + 10,
            value=latest_year + 1,
            step=1,
            key="forecast_year",
        )
    with county_col:
        county_filter = st.selectbox(
            "County",
            ["All counties", *counties],
            key="county_filter",
        )
    submitted = st.form_submit_button(
        "Generate forecast",
        type="primary",
        key="generate_forecast",
    )

if "county_forecast_results" not in st.session_state or submitted:
    st.session_state["county_forecast_results"] = build_county_forecasts(
        historical,
        int(target_year),
    )

forecasts = st.session_state["county_forecast_results"]
if int(forecasts["Forecast_Year"].iloc[0]) != int(target_year):
    forecasts = build_county_forecasts(historical, int(target_year))
    st.session_state["county_forecast_results"] = forecasts

visible_forecasts = forecasts
if county_filter != "All counties":
    visible_forecasts = forecasts[forecasts["County"] == county_filter]

total_production = visible_forecasts["Forecast_Production"].sum()
average_mae = visible_forecasts["Validation_MAE"].mean()

with st.container(horizontal=True):
    st.metric("Counties forecast", f"{len(visible_forecasts):,}")
    st.metric(
        f"Estimated production in {int(target_year)}",
        f"{total_production:,.0f} tonnes",
    )
    st.metric("Mean backtest MAE", f"{average_mae:,.0f} tonnes")

st.subheader(f"County production estimates for {int(target_year)}")
st.bar_chart(
    visible_forecasts.head(15).sort_values("Forecast_Production"),
    x="County",
    y="Forecast_Production",
    horizontal=True,
    alt=f"Top county maize production estimates for {int(target_year)}",
)

if county_filter == "All counties":
    st.subheader("National historical production")
    national_history = (
        historical.groupby("Year", as_index=False)["Production_Tonnes"]
        .sum()
        .rename(columns={"Production_Tonnes": "Observed production"})
        .set_index("Year")
    )
    national_history["Forecast production"] = float("nan")
    forecast_row = pd.DataFrame(
        {
            "Observed production": [float("nan")],
            "Forecast production": [float(total_production)],
        },
        index=pd.Index([int(target_year)], name="Year"),
    )
    national_history = pd.concat([national_history, forecast_row]).sort_index()
    st.line_chart(
        national_history,
        alt="Observed national maize production and forecast",
    )
else:
    st.subheader(f"{county_filter} production history")
    county_history = historical.loc[
        historical["County"] == county_filter,
        ["Year", "Production_Tonnes"],
    ].rename(columns={"Production_Tonnes": "Observed production"}).set_index("Year")
    county_forecast = visible_forecasts.iloc[0]
    forecast_row = pd.DataFrame(
        {
            "Observed production": [float("nan")],
            "Forecast production": [county_forecast["Forecast_Production"]],
        },
        index=pd.Index([int(target_year)], name="Year"),
    )
    county_history["Forecast production"] = float("nan")
    county_history = pd.concat([county_history, forecast_row]).sort_index()
    st.line_chart(
        county_history,
        alt=f"Historical and estimated maize production for {county_filter}",
    )

st.subheader("Forecast details")
st.dataframe(
    visible_forecasts.rename(
        columns={
            "Forecast_Year": "Forecast year",
            "Forecast_Production": "Forecast production (tonnes)",
            "Validation_MAE": "Backtest MAE (tonnes)",
            "Last_Observed_Year": "Latest observed year",
            "Last_Observed_Production": "Latest observed production (tonnes)",
            "Historical_Years": "Historical observations",
            "Method": "Selected method",
        }
    ),
    hide_index=True,
    alt="County production estimates and historical backtest errors",
)
st.download_button(
    "Download forecast CSV",
    data=visible_forecasts.to_csv(index=False),
    file_name=f"kenya_maize_forecast_{int(target_year)}.csv",
    mime="text/csv",
)

st.info(
    "These are historical-only estimates, not official forecasts. "
    "The workbook covers 2012–2018 and 2020, with no 2019 record. "
    "Backtest MAE summarizes errors on later observed records; "
    "accuracy can be lower for forecasts several years beyond the available data."
)
