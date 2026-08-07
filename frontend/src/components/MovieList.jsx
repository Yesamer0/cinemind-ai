import MovieCard from "./MovieCard";

function MovieList({ movies }) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
        gap: "25px",
        maxWidth: "1200px",
        margin: "40px auto"
      }}
    >
      {movies.map((movie, index) => (
        <MovieCard
          key={index}
          movie={movie}
        />
      ))}
    </div>
  );
}

export default MovieList;