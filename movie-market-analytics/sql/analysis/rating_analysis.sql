SELECT
    CASE
        WHEN f.rating >= 9 THEN '9.0-10.0'
        WHEN f.rating >= 8 THEN '8.0-8.9'
        WHEN f.rating >= 7 THEN '7.0-7.9'
        WHEN f.rating >= 6 THEN '6.0-6.9'
        ELSE '<6.0'
    END AS rating_bucket,
    COUNT(*) AS movie_count,
    ROUND(AVG(f.vote_count), 0) AS avg_votes
FROM fact_movie_rating f
GROUP BY rating_bucket
ORDER BY rating_bucket DESC;
