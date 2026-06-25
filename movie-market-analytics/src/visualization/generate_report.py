from src.analysis.analyze_movies_pandas import load_movies_dataframe, summarize_movies
from src.config import settings
from src.utils.logger import logger


def main() -> None:
    settings.REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_movies_dataframe()
    if df.empty:
        logger.warning("No movie data found. Please run the ETL pipeline first.")
        return
    summary = summarize_movies(df)
    report = [
        "# Movie Market Analysis Report",
        "",
        "## Dataset Overview",
        "",
        f"- Total movies: {summary.get('total_movies', 0)}",
        f"- Average rating: {summary.get('avg_rating', 'N/A')}",
        f"- Total votes: {summary.get('total_votes', 0)}",
        f"- Year range: {summary.get('year_min', 'N/A')} - {summary.get('year_max', 'N/A')}",
        "",
        "## Generated Figures",
        "",
        "- `avg_rating_by_genre.png`",
        "- `movie_count_by_country.png`",
        "- `movie_count_by_year.png`",
        "- `rating_vs_vote_count.png`",
        "- `rating_distribution.png`",
    ]
    output_path = settings.REPORT_DIR / "analysis_report.md"
    output_path.write_text("\n".join(report), encoding="utf-8")
    logger.info("Saved report: %s", output_path)


if __name__ == "__main__":
    main()
