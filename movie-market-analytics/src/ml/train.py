
from src.analysis.analyze_movies_pandas import load_movies_dataframe
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

from src.config import settings
from src.ml.features import build_features
from src.ml.model import get_model


def train():
    print("Loading data from MySQL...")

    df = load_movies_dataframe()

    if df.empty:
        raise ValueError("No data found in database")

    print("[DEBUG] Raw data shape:", df.shape)

    X, y, mlb = build_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = get_model()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print("\n===== MODEL EVALUATION =====")
    print("MAE:", mean_absolute_error(y_test, preds))
    print("R2 :", r2_score(y_test, preds))

    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, settings.OUTPUT_DIR / "model.pkl")
    joblib.dump(mlb, settings.OUTPUT_DIR / "genre_encoder.pkl")

    print("[OK] Model saved to outputs/")
    

if __name__ == "__main__":
    train()