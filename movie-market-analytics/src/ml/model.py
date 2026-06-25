from sklearn.ensemble import RandomForestRegressor


def get_model():
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    return model
