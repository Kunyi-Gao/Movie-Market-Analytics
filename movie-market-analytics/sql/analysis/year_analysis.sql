SELECT
    m.release_year,
    COUNT(*) AS movie_count,
    ROUND(AVG(f.rating), 2) AS avg_rating,
    SUM(f.vote_count) AS total_votes
FROM dim_movie m
JOIN fact_movie_rating f ON m.movie_id = f.movie_id
GROUP BY m.release_year
ORDER BY m.release_year;
