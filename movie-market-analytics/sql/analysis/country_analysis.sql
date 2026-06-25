SELECT
    m.country,
    COUNT(*) AS movie_count,
    ROUND(AVG(f.rating), 2) AS avg_rating,
    SUM(f.vote_count) AS total_votes
FROM dim_movie m
JOIN fact_movie_rating f ON m.movie_id = f.movie_id
GROUP BY m.country
ORDER BY movie_count DESC, avg_rating DESC;
