import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

from src.utils.logger import logger

def build_features(df: pd.DataFrame):
    df = df.copy()

    # ===== numeric features =====
    df["release_year"] = df["release_year"].fillna(df["release_year"].median())
    df["duration"] = df["duration"].fillna(df["duration"].median())
    df["vote_count"] = df["vote_count"].fillna(0)

    # ===== country encoding =====
    df["country"] = df["country"].fillna("Unknown")
    country_dummies = pd.get_dummies(df["country"], prefix="country")

    # ===== genre multi-hot =====
    mlb = MultiLabelBinarizer()

    df["genres_list"] = df["genres"].fillna("").apply(
        lambda x: [g.strip() for g in x.split(",") if g.strip()]
    )

    genre_matrix = mlb.fit_transform(df["genres_list"])
    genre_df = pd.DataFrame(genre_matrix, columns=mlb.classes_)

    # ===== final feature set =====
    X = pd.concat([
        df[["release_year", "duration", "vote_count"]],
        country_dummies,
        genre_df
    ], axis=1)

    y = df["rating"]

    print("[DEBUG] Feature shape:", X.shape)
    print("[DEBUG] Target shape:", y.shape)

    return X, y, mlb