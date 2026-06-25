import joblib
import pandas as pd

from src.ml.features import build_features


model = joblib.load("outputs/model.pkl")


def predict_rating(df: pd.DataFrame):
    X, _, _ = build_features(df)
    preds = model.predict(X)
    return preds