# API Documentation

Base URL: `http://127.0.0.1:5000/api/v1`

## Health

`GET /health`

Response:
- `success: true`
- `data: { status: "ok" }`

## Movies

List movies:
`GET /movies?page=1&page_size=20&genre=Drama&country=China&year_min=2010&year_max=2024&sort_by=rating&order=desc`

Supported `sort_by` values:
- `rating`
- `vote_count`
- `year`
- `title`
- `popularity`

Get a single movie:
`GET /movies/<movie_id>`

## Genres

`GET /genres`

## Stats

- `GET /stats/genres`
- `GET /stats/years`
- `GET /stats/countries`
- `GET /stats/popularity`

## Prediction

`POST /predict/rating`

Request body:
```json
[
  {
    "genres": "Action, Drama",
    "release_year": 2022,
    "duration": 120,
    "vote_count": 3500,
    "country": "USA"
  }
]
```

Response:
- `success: true`
- `data.predictions`: list of predicted rating values

## Visuals

`GET /visuals/<filename>.png`

Return:
- PNG image file from `outputs/figures/`
