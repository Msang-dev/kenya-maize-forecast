# Kenya maize production forecast

The Streamlit dashboard forecasts maize production by county using the historical records in `data/Maize-Production-2012-2020-Combined.xlsx`.

## Run the dashboard

```powershell
python -m pip install -r requirements.txt
streamlit run app.py
```

Choose a forecast year and county, then select **Generate forecast**. The dashboard shows county estimates, historical production, backtest error, and a CSV download.

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository. Include `app.py`, `src/`, `data/`, and `requirements.txt`; do not commit `.venv/`, credentials, or `.streamlit/secrets.toml`.
2. Sign in at [share.streamlit.io](https://share.streamlit.io/) using the GitHub account that can access the repository.
3. Select **Create app**, choose the repository and branch, set the main file to `app.py`, then deploy.
4. For a public app, make the app public in its Streamlit sharing settings. A public app can be viewed by anyone; if the GitHub repository is also public, its source code and workbook are public too.

The app reads the workbook from the checked-in `data/` directory, so no secrets or external services are required.

The optional packages in `requirements-optional.txt` are for the separate training, mapping, weather, SHAP, and report modules; they are not needed to run the deployed dashboard.

## Forecast method

For each county, the system compares a recent three-observation average, the latest observed production, and a linear trend. It selects the method with the lowest expanding-window historical mean absolute error, then refits that method on all available records to forecast the requested year. Negative estimates are constrained to zero.

The workbook contains records for 2012–2018 and 2020; 2019 is missing. Estimates are based on production history only, so they do not account for weather, planted area, or other future conditions. The backtest MAE summarizes errors on later observed records and is not a guarantee of future accuracy, especially for years far beyond the historical data.

Run the forecast tests with:

```powershell
python -m unittest discover -s tests -v
```
