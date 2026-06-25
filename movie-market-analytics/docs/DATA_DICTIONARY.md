# Data Dictionary

## dim_movie

| Column | Meaning |
|---|---|
| movie_id | Surrogate primary key |
| douban_id | Source movie identifier |
| title | Movie title |
| release_year | Release year |
| country | Country or region |
| director | Director name |
| actors | Main actors |
| duration | Duration in minutes |
| language | Movie language |
| summary | Short summary |

## dim_genre

| Column | Meaning |
|---|---|
| genre_id | Surrogate primary key |
| genre_name | Genre name |

## fact_movie_rating

| Column | Meaning |
|---|---|
| rating | Douban-style movie rating |
| vote_count | Number of votes |
| popularity_score | rating * vote_count |
| collected_at | Load timestamp |
