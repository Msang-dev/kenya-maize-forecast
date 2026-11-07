import json
import plotly.express as px


def create_county_map(
    map_df,
    geojson_path="data/kenya_counties.geojson"
):

    with open(
        geojson_path,
        "r",
        encoding="utf-8"
    ) as f:

        counties = json.load(f)

    fig = px.choropleth_mapbox(
        map_df,
        geojson=counties,
        locations="County",
        featureidkey="properties.COUNTY",
        color="Forecast_Production",
        hover_name="County",
        color_continuous_scale="YlGn",
        mapbox_style="carto-positron",
        zoom=5.5,
        center={
            "lat": 0.3,
            "lon": 37.9
        },
        opacity=0.7
    )

    fig.update_layout(
        margin={
            "r": 0,
            "t": 0,
            "l": 0,
            "b": 0
        }
    )

    return fig