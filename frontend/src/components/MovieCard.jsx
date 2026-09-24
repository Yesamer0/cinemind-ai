import { Link } from "react-router-dom";

function MovieCard({ movie }) {

  const posterUrl =
    movie.poster_path &&
    typeof movie.poster_path === "string" &&
    movie.poster_path.startsWith("/")
      ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
      : null;


  // Different recommendation endpoints use different score names.
  const aiScore =
    movie.score ??
    movie.hybrid_score ??
    movie.similarity ??
    null;


  return (
    <Link
      to={`/movie/${movie.id}`}
      className="movie-card-link"
    >

      <article className="movie-card">

        <div className="movie-poster-container">

          {posterUrl ? (
            <img
              className="movie-poster"
              src={posterUrl}
              alt={movie.title}
              loading="lazy"
              onError={(event) => {
                event.currentTarget.style.display = "none";

                const fallback =
                  event.currentTarget.nextElementSibling;

                if (fallback) {
                  fallback.style.display = "flex";
                }
              }}
            />
          ) : null}


          <div
            className="poster-fallback"
            style={{
              display: posterUrl ? "none" : "flex"
            }}
          >
            <span>🎬</span>
            <p>No Poster</p>
          </div>


          {aiScore !== null && (
            <div className="ai-score-badge">
              🤖 {Number(aiScore).toFixed(2)}
            </div>
          )}

        </div>


        <div className="movie-card-content">

          <h3 className="movie-card-title">
            {movie.title}
          </h3>


          <p className="movie-card-overview">
            {movie.overview ||
              "No description available for this movie."}
          </p>


          <div className="movie-card-footer">

            {movie.rating !== undefined &&
              movie.rating !== null ? (
                <span className="movie-rating">
                  ⭐ {Number(movie.rating).toFixed(1)}
                </span>
              ) : (
                <span className="movie-discover">
                  View details
                </span>
              )}

            <span className="movie-arrow">
              →
            </span>

          </div>

        </div>

      </article>

    </Link>
  );
}

export default MovieCard;