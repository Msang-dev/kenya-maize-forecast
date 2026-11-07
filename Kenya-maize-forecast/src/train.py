from src.data import load_data
from src.data import reshape_data
from src.features import create_features
from src.model import train_model

df = load_data(
    "data/Maize-Production-2012-2020-Combined.xlsx"
)

df = reshape_data(df)

df = create_features(df)

train_model(df)

print(
    "✅ Model Trained Successfully"
)