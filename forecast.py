import numpy as np


FORECAST_METHODS = (
    "recent_average",
    "last_observation",
    "linear_trend",
)


def _predict(method, years, production, target_year):
    years = np.asarray(years, dtype=float)
    production = np.asarray(production, dtype=float)

    if method == "recent_average":
        prediction = float(np.mean(production[-3:]))
    elif method == "last_observation":
        prediction = float(production[-1])
    elif method == "linear_trend":
        slope, intercept = np.polyfit(years, production, deg=1)
        prediction = float(slope * target_year + intercept)
    else:
        raise ValueError(f"Unknown forecast method: {method}")

    return max(0.0, prediction)


def select_forecast_method(years, production):
    """Choose a county's method using expanding-window, one-year backtests."""
    years = np.asarray(years, dtype=float)
    production = np.asarray(production, dtype=float)
    errors = {method: [] for method in FORECAST_METHODS}

    for split in range(3, len(production)):
        for method in FORECAST_METHODS:
            prediction = _predict(
                method,
                years[:split],
                production[:split],
                years[split],
            )
            errors[method].append(abs(prediction - production[split]))

    mean_absolute_errors = {
        method: float(np.mean(method_errors))
        for method, method_errors in errors.items()
    }
    method = min(
        FORECAST_METHODS,
        key=lambda candidate: mean_absolute_errors[candidate],
    )
    return method, mean_absolute_errors[method]


def forecast_from_history(years, production, target_year):
    """Forecast production from one county's dated historical observations."""
    years = np.asarray(years, dtype=float)
    production = np.asarray(production, dtype=float)

    if len(years) != len(production) or len(production) < 4:
        raise ValueError("At least four matching annual observations are required.")
    if not np.isfinite(years).all() or not np.isfinite(production).all():
        raise ValueError("Historical years and production values must be finite.")
    if np.any(np.diff(years) <= 0):
        raise ValueError("Historical years must be unique and in ascending order.")
    if np.any(production < 0):
        raise ValueError("Historical production values cannot be negative.")
    if target_year <= years[-1]:
        raise ValueError("The forecast year must be later than the latest historical year.")

    method, validation_mae = select_forecast_method(years, production)
    prediction = _predict(method, years, production, target_year)
    return prediction, method, validation_mae
