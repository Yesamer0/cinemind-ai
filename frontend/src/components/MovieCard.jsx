function MovieCard({ movie }) {
  return (
    <div
      style={{
        border: "1px solid gray",
        borderRadius: "10px",
        padding: "15px",
        marginBottom: "15px"
      }}
    >
      <h2>{movie.title}</h2>

      <p>{movie.overview}</p>

      <strong>
        ⭐ Score: {movie.score}
      </strong>
    </div>
  );
}

export default MovieCard;