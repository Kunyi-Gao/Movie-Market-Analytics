# Movie Market Analytics

A presentation-ready movie market analytics project built with Python, MySQL, Flask, Pandas, and Matplotlib.
It demonstrates a compact, reproducible end-to-end analytics workflow: ingestion → dimensional DB → analysis → visualization → predictive extension.

## Project Summary

Purpose: provide a compact, reproducible analytics platform over movie metadata.

This project collects, cleans, and loads movie metadata into a dimensional MySQL model and exposes a compact analysis platform (API, visuals, and an optional predictive module).

Key components:
- ETL pipeline for CSV ingestion and cleaning
- Dimensional MySQL schema (facts + dimensions)
- Flask REST API with search, filtering and pagination
- Analysis and visualization using Pandas and Matplotlib
- Predictive analytics module with model artifacts saved for API consumption

Key Highlights
Purpose: quick, high-signal bullets for reviewers.
- End-to-end system: ETL -> dimensional DB -> API -> visualization -> predictive module
- ETL + database design: idempotent loads and star schema for efficient aggregations
- API engineering: pagination, filtering, input validation, and lazy model loading
- Feature engineering: multi-label genre encoding, categorical encoding, and conservative imputation
- Predictive analytics: reproducible scikit-learn training with RandomForest baseline

Motivation / Problem Statement
--------------------------------

Purpose: explain why the project matters and the decision context.

The media market is noisy and competitive. This project shows how structured metadata (titles, genres, years, countries, ratings, vote counts) can be transformed into actionable analytics for discovery, aggregation, and lightweight prediction.

This project supports:
- fast discovery (search + filters)
- aggregate statistics for strategic insight (genre, country, year)
- reproducible visualizations for storytelling
- a lightweight predictive extension to estimate rating trends

System Design Overview
------------------------

Purpose: summarize the architecture and major components.

Logical flow: ETL -> Dimensional DB -> API -> Analysis & Visualization -> Predictive Module

- `src/pipelines`, `src/scripts`: ingest and transform CSVs for loading
- `sql/ddl`: star-schema (dimensions + facts) for efficient analytical queries
- `src/api`: Flask app exposing search, stats, visuals, and a prediction endpoint
- `src/analysis`, `src/visualization`: reproducible analyses and plotting that produce assets in `outputs/`
- `src/ml`: feature engineering, training, and model artifacts consumed by the API

Design rationale: MySQL and a dimensional model were chosen for accessibility and efficient aggregations; Flask provides a small, inspectable API surface.

Predictive Analytics Module
---------------------------

Purpose: describe the predictive extension and its role in the system.

The ML component is a predictive analytics module built on the ETL and analytical database. It produces reproducible model artifacts consumed by the API.

Feature engineering (in `src/ml/features.py`):

- Multi-label genre encoding via `MultiLabelBinarizer` (multi-hot) to preserve multiple genres per movie
- Categorical encoding: `country` imputed to "Unknown" and one-hot encoded with `pandas.get_dummies`
- Missing values: `release_year` and `duration` imputed with the median; `vote_count` defaulted to 0

Model justification:

- `RandomForestRegressor` (in `src/ml/model.py`) is used as a reproducible baseline: it handles non-linear relationships, mixed feature types, and performs well on tabular datasets

Evaluation:

- `src/ml/train.py` performs a train/test split and prints MAE and R² as baseline metrics; these are quick, interpretable checks of predictive signal

ML Design Philosophy:

- Favor simple, transparent transforms and conservative imputation to reduce overfitting
- Prefer interpretable features and models that can inform applied analytics
- Save artifacts (`model.pkl`, `genre_encoder.pkl`) to `outputs/` and load them lazily in the API for reproducible predictions

Technical Highlights

Purpose: list the key engineering achievements.

- Modular ETL and idempotent loads (`src/pipelines`)
- Dimensional schema for fast aggregations (`sql/ddl`)
- API with pagination, filtering, validation, and lazy model loading (`src/api`)
- Reproducible training with fixed seeds and saved artifacts (`src/ml` -> `outputs/`)

What This Project Demonstrates
-------------------------------

Purpose: state the practical skills and outcomes the project illustrates.

- Designed and implemented an ETL pipeline and dimensional schema for analytics
- Engineered feature transforms and reproducible model artifacts for predictive use
- Implemented a compact Flask API with robust input validation and pagination
- Integrated analysis, visualization, and prediction into a single reproducible workflow

Repository Layout

Purpose: quick reference to important folders.

- `data/` — raw, processed, and sample datasets
- `sql/` — DDL and analysis queries
- `src/api/` — Flask application and route definitions
- `src/pipelines/` — extract, transform, and load pipeline
- `src/db/` — MySQL helper and database integration
- `src/ml/` — feature engineering and model training utilities
- `src/visualization/` — plotting and report generation
- `tests/` — automated tests
- `docs/` — API documentation and data dictionary
- `outputs/` — generated figures, reports, and model artifacts

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Update `.env` with your MySQL credentials and database settings.

> If you prefer a package-focused install, `pyproject.toml` is also provided for optional packaging support.

## Database Initialization

Create the project database and schema:

```bash
mysql -u root -p < sql/ddl/01_create_database.sql
mysql -u root -p movie_market_v2 < sql/ddl/02_create_tables.sql
mysql -u root -p movie_market_v2 < sql/ddl/03_create_indexes.sql
```

## Data Pipeline

Run the ETL pipeline to ingest sample data, clean it, and load it into MySQL:

```bash
python -m src.pipelines.run_pipeline
```

Alternatively, import existing CSV data directly:

```bash
python -m src.scripts.import_movies_from_csv
```

## API Usage

Start the Flask API:

```bash
python -m src.api.app
```

Available endpoints:

- `GET /api/v1/health`
- `GET /api/v1/movies`
- `GET /api/v1/movies/<movie_id>`
- `GET /api/v1/genres`
- `GET /api/v1/stats/genres`
- `GET /api/v1/stats/years`
- `GET /api/v1/stats/countries`
- `GET /api/v1/stats/popularity`
- `GET /api/v1/visuals/<filename>.png`
- `POST /api/v1/predict/rating`

Example movie query:

```text
GET http://127.0.0.1:5000/api/v1/movies?page=1&page_size=10&genre=Drama&sort_by=rating&order=desc
```

## Model Training

Train the regression model and save artifacts to `outputs/`:

```bash
python -m src.ml.train
```

## Testing

Run the test suite with:

```bash
pytest
```

## Notes

This repository is designed to be presentation-ready rather than production-scale. The code emphasizes clarity, reproducibility, and end-to-end analytics workflow completeness.

One-line summary: This project demonstrates end-to-end data system design with predictive analytics integration.

## Documentation

- `docs/API.md`
- `docs/DATA_DICTIONARY.md`
- `docs/ERD.md`
