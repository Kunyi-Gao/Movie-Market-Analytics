SELECT
    g.genre_name,
    COUNT(DISTINCT m.movie_id) AS movie_count,
    ROUND(AVG(f.rating), 2) AS avg_rating,
    SUM(f.vote_count) AS total_votes
FROM dim_movie m
JOIN fact_movie_rating f ON m.movie_id = f.movie_id
JOIN bridge_movie_genre b ON m.movie_id = b.movie_id
JOIN dim_genre g ON b.genre_id = g.genre_id
GROUP BY g.genre_name
ORDER BY avg_rating DESC, movie_count DESC;
