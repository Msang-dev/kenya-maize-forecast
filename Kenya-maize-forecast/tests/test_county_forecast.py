import unittest

import pandas as pd

from src.county_forecast import build_county_forecasts
from src.data import reshape_data
from src.forecast import forecast_from_history


class ForecastTests(unittest.TestCase):
    def test_linear_history_is_selected_when_it_backtests_best(self):
        years = [2015, 2016, 2017, 2018, 2019, 2020]
        production = [100, 110, 120, 130, 140, 150]

        forecast, method, mae = forecast_from_history(years, production, 2022)

        self.assertEqual(method, "linear_trend")
        self.assertAlmostEqual(forecast, 170.0)
        self.assertAlmostEqual(mae, 0.0)

    def test_forecast_year_must_be_after_history(self):
        with self.assertRaisesRegex(ValueError, "later than"):
            forecast_from_history([2017, 2018, 2019, 2020], [1, 2, 3, 4], 2020)

    def test_builds_forecasts_for_all_workbook_counties(self):
        forecasts = build_county_forecasts(target_year=2021)

        self.assertEqual(len(forecasts), 47)
        self.assertEqual(forecasts["County"].nunique(), 47)
        self.assertEqual(forecasts["Forecast_Year"].unique().tolist(), [2021])
        self.assertTrue((forecasts["Forecast_Production"] >= 0).all())
        self.assertTrue((forecasts["Validation_MAE"] >= 0).all())
        self.assertEqual(set(forecasts["Historical_Years"]), {8})

    def test_duplicate_county_year_records_are_rejected(self):
        history = pd.DataFrame(
            {
                "County": ["Example"] * 4,
                "Year": [2017, 2018, 2018, 2020],
                "Production_Tonnes": [10, 11, 12, 14],
            }
        )

        with self.assertRaisesRegex(ValueError, "duplicate"):
            build_county_forecasts(history, 2021)

    def test_reshape_strips_county_name_whitespace(self):
        source = pd.DataFrame(
            {
                "County": [" Nairobi "],
                "Year": [2020],
                "Indicator": ["Production (MT)"],
                "Value": [12.0],
            }
        )

        result = reshape_data(source)

        self.assertEqual(result.loc[0, "County"], "Nairobi")


if __name__ == "__main__":
    unittest.main()
