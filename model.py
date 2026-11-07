import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

FEATURES = [
    "Year",
    "Area_Hectares",
    "Yield",
    "Growth_Rate",
    "Rolling_Mean"
]


def train_model(df):

    X = df[FEATURES]
    y = df["Production_Tonnes"]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )
    )

    model = RandomForestRegressor(
        n_estimators=500,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print(
        "MAE:",
        mean_absolute_error(y_test, preds)
    )

    print(
        "R2:",
        r2_score(y_test, preds)
    )

    joblib.dump(
        model,
        "models/maize_model.pkl"
    )

    return model