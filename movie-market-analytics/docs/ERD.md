# ERD

```mermaid
erDiagram
    dim_movie ||--o{ fact_movie_rating : has
    dim_movie ||--o{ bridge_movie_genre : belongs_to
    dim_genre ||--o{ bridge_movie_genre : includes

    dim_movie {
        bigint movie_id PK
        string douban_id
        string title
        int release_year
        string country
        string director
        int duration
    }

    dim_genre {
        bigint genre_id PK
        string genre_name
    }

    bridge_movie_genre {
        bigint movie_id FK
        bigint genre_id FK
    }

    fact_movie_rating {
        bigint rating_id PK
        bigint movie_id FK
        decimal rating
        int vote_count
        decimal popularity_score
    }
```
