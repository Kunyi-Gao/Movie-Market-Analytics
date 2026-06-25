USE movie_market_v2;

DROP TABLE IF EXISTS bridge_movie_genre;
DROP TABLE IF EXISTS fact_movie_rating;
DROP TABLE IF EXISTS dim_genre;
DROP TABLE IF EXISTS dim_movie;

CREATE TABLE dim_movie (
    movie_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    douban_id VARCHAR(50) UNIQUE,
    title VARCHAR(255) NOT NULL,
    release_year INT,
    country VARCHAR(100),
    director VARCHAR(255),
    actors TEXT,
    duration INT,
    language VARCHAR(100),
    summary TEXT,
    url VARCHAR(500),
    cover_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_movie_title_year_director (title, release_year, director)
);

CREATE TABLE dim_genre (
    genre_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    genre_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE fact_movie_rating (
    rating_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    movie_id BIGINT NOT NULL,
    rating DECIMAL(3,1),
    vote_count INT,
    popularity_score DECIMAL(12,2),
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES dim_movie(movie_id) ON DELETE CASCADE,
    UNIQUE KEY uq_fact_movie_rating_movie (movie_id)
);

CREATE TABLE bridge_movie_genre (
    movie_id BIGINT NOT NULL,
    genre_id BIGINT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES dim_movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES dim_genre(genre_id) ON DELETE CASCADE
);
