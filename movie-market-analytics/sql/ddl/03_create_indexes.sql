USE movie_market_v2;

CREATE INDEX idx_dim_movie_year ON dim_movie(release_year);
CREATE INDEX idx_dim_movie_country ON dim_movie(country);
CREATE INDEX idx_fact_rating ON fact_movie_rating(rating);
CREATE INDEX idx_fact_vote_count ON fact_movie_rating(vote_count);
CREATE INDEX idx_genre_name ON dim_genre(genre_name);
