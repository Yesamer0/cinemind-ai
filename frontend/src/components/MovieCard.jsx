import { Link } from "react-router-dom";

function MovieCard({ movie }) {
  return (
    <Link
      to={`/movie/${movie.id}`}
      style={{
        textDecoration: "none",
        color: "inherit"
      }}
    >
      <div
        style={{
          border: "1px solid gray",
          borderRadius: "10px",
          padding: "15px",
          marginBottom: "15px",
          cursor: "pointer"
        }}
      >
        <h2>{movie.title}</h2>

        <p>{movie.overview}</p>

        <strong>⭐ Score: {movie.score}</strong>
      </div>
    </Link>
  );
}

export default MovieCard;