SELECT
    m.title,
    m.release_year,
    m.country,
    f.rating,
    f.vote_count,
    f.popularity_score
FROM dim_movie m
JOIN fact_movie_rating f ON m.movie_id = f.movie_id
ORDER BY f.popularity_score DESC, f.rating DESC
LIMIT 20;
