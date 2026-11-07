import requests

COUNTIES = {

    "Nakuru": (-0.3031, 36.08),
    "Trans Nzoia": (1.0567, 34.95),
    "Uasin Gishu": (0.5143, 35.27),
    "Bungoma": (0.5635, 34.56),
    "Meru": (0.0470, 37.65),
    "Embu": (-0.5390, 37.45)

}


def get_weather(county):

    lat, lon = COUNTIES.get(
        county,
        (-0.3031, 36.08)
    )

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&daily=precipitation_sum,"
        "temperature_2m_max"
        "&forecast_days=7"
    )

    response = requests.get(
        url,
        timeout=20
    )

    response.raise_for_status()

    return response.json()