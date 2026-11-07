SEEDS = {

    "Nakuru": "H6213",
    "Trans Nzoia": "DK777",
    "Uasin Gishu": "WH505",
    "Bungoma": "H628",
    "Meru": "DUMA43",
    "Embu": "H516"

}


def recommend_seed(county):

    return SEEDS.get(
        county,
        "H6210"
    )