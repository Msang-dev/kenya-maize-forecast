import pandas as pd
import shap
import joblib

model = joblib.load(
    "models/maize_model.pkl"
)

explainer = shap.TreeExplainer(
    model
)


def get_shap_values(features):

    df = pd.DataFrame(
        [features]
    )

    return explainer(df)