from pathlib import Path

import numpy as np
import pandas as pd

from src.data import load_data, reshape_data
from src.forecast import forecast_from_history


DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "Maize-Production-2012-2020-Combined.xlsx"
)


def build_county_forecasts(data=None, target_year=None):
    """Forecast each county using its historical production observations."""
    if data is None:
        data = reshape_data(load_data(str(DATA_FILE)))

    required = {"County", "Year", "Production_Tonnes"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(
            "County forecasting requires columns: "
            + ", ".join(sorted(missing))
        )

    history = data[["County", "Year", "Production_Tonnes"]].copy()
    history["Year"] = pd.to_numeric(history["Year"], errors="coerce")
    history["Production_Tonnes"] = pd.to_numeric(
        history["Production_Tonnes"], errors="coerce"
    )

    if history[["County", "Year", "Production_Tonnes"]].isna().any().any():
        raise ValueError("County, year, and production values cannot be blank.")
    if not np.isfinite(history["Year"]).all() or not np.isfinite(
        history["Production_Tonnes"]
    ).all():
        raise ValueError("Year and production values must be finite numbers.")
    if not np.equal(history["Year"], np.floor(history["Year"])).all():
        raise ValueError("Historical years must be whole calendar years.")
    if history["County"].astype(str).str.strip().eq("").any():
        raise ValueError("County names cannot be blank.")
    if history.duplicated(["County", "Year"]).any():
        raise ValueError("Historical data has duplicate county-year records.")
    if (history["Production_Tonnes"] < 0).any():
        raise ValueError("Historical production values cannot be negative.")

    history["County"] = history["County"].astype(str).str.strip()
    history = history.sort_values(["County", "Year"])
    latest_year = int(history["Year"].max())
    if target_year is None:
        target_year = latest_year + 1
    if isinstance(target_year, bool) or int(target_year) != target_year:
        raise ValueError("The forecast year must be a whole calendar year.")
    target_year = int(target_year)
    if target_year <= latest_year:
        raise ValueError(
            f"The forecast year must be later than the latest historical year ({latest_year})."
        )

    forecasts = []
    for county, county_history in history.groupby("County", sort=True):
        if len(county_history) < 4:
            raise ValueError(
                f"{county} has fewer than four valid historical observations."
            )

        years = county_history["Year"].to_numpy(dtype=float)
        production = county_history["Production_Tonnes"].to_numpy(dtype=float)
        prediction, method, validation_mae = forecast_from_history(
            years,
            production,
            target_year,
        )
        forecasts.append(
            {
                "County": county,
                "Forecast_Year": target_year,
                "Forecast_Production": prediction,
                "Method": method,
                "Validation_MAE": validation_mae,
                "Last_Observed_Year": int(years[-1]),
                "Last_Observed_Production": float(production[-1]),
                "Historical_Years": len(years),
            }
        )

    return pd.DataFrame(forecasts).sort_values(
        "Forecast_Production", ascending=False
    ).reset_index(drop=True)
