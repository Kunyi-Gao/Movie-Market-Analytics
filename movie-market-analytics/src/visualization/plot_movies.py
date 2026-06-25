from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.analysis.analyze_movies_pandas import load_movies_dataframe
from src.config import settings
from src.utils.logger import logger


def prepare_output_dir() -> None:
    settings.FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(filename: str) -> None:
    output_path = settings.FIGURE_DIR / filename
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info("Saved figure: %s", output_path)


def explode_genres(df: pd.DataFrame) -> pd.DataFrame:
    temp = df.copy()
    temp["genre"] = temp["genres"].fillna("").str.split(", ")
    return temp.explode("genre").query("genre != ''")


def plot_avg_rating_by_genre(df: pd.DataFrame) -> None:
    genre_df = explode_genres(df)
    summary = genre_df.groupby("genre")["rating"].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    summary.plot(kind="bar")
    plt.title("Average Rating by Genre")
    plt.xlabel("Genre")
    plt.ylabel("Average Rating")
    plt.xticks(rotation=45, ha="right")
    save_figure("avg_rating_by_genre.png")


def plot_movie_count_by_country(df: pd.DataFrame) -> None:
    counts = df["country"].value_counts()
    plt.figure(figsize=(8, 5))
    counts.plot(kind="bar")
    plt.title("Movie Count by Country / Region")
    plt.xlabel("Country / Region")
    plt.ylabel("Movie Count")
    plt.xticks(rotation=30, ha="right")
    save_figure("movie_count_by_country.png")


def plot_movie_count_by_year(df: pd.DataFrame) -> None:
    counts = df.groupby("release_year")["title"].count().sort_index()
    plt.figure(figsize=(10, 5))
    counts.plot(kind="line", marker="o")
    plt.title("Movie Count by Year")
    plt.xlabel("Year")
    plt.ylabel("Movie Count")
    plt.grid(True, alpha=0.3)
    save_figure("movie_count_by_year.png")


def plot_rating_vs_votes(df: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 6))
    plt.scatter(df["vote_count"], df["rating"])
    plt.title("Rating vs Vote Count")
    plt.xlabel("Vote Count")
    plt.ylabel("Rating")
    plt.grid(True, alpha=0.3)
    save_figure("rating_vs_vote_count.png")


def plot_rating_distribution(df: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5))
    df["rating"].plot(kind="hist", bins=10)
    plt.title("Rating Distribution")
    plt.xlabel("Rating")
    save_figure("rating_distribution.png")


def main() -> None:
    prepare_output_dir()
    df = load_movies_dataframe()
    if df.empty:
        logger.warning("No movie data found. Please run the ETL pipeline first.")
        return
    plot_avg_rating_by_genre(df)
    plot_movie_count_by_country(df)
    plot_movie_count_by_year(df)
    plot_rating_vs_votes(df)
    plot_rating_distribution(df)
    logger.info("Movie visualizations completed.")


if __name__ == "__main__":
    main()
