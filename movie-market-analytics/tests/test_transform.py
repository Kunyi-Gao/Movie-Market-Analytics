import pandas as pd

from src.pipelines.transform import clean_movies_dataframe, split_multi_value


def test_split_multi_value_handles_multiple_separators():
    assert split_multi_value("Drama / Crime, Action") == ["Action", "Crime", "Drama"]


def test_clean_movies_dataframe_removes_duplicates_and_adds_popularity():
    df = pd.DataFrame([
        {
            "title": "A", "year": 2020, "region": "China", "genre": "Drama", "rating": 8.0,
            "vote_count": 100, "director": "D", "douban_id": "1", "url": "u", "cover_url": "c",
            "actors": "x", "duration": 100, "language": "Chinese", "summary": "s",
        },
        {
            "title": "A", "year": 2020, "region": "China", "genre": "Drama", "rating": 8.0,
            "vote_count": 100, "director": "D", "douban_id": "1", "url": "u", "cover_url": "c",
            "actors": "x", "duration": 100, "language": "Chinese", "summary": "s",
        },
    ])
    cleaned = clean_movies_dataframe(df)
    assert len(cleaned) == 1
    assert "popularity_score" in cleaned.columns
    assert cleaned.loc[0, "popularity_score"] == 800.0
