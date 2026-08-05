import MovieCard from "./MovieCard";

function MovieList({ movies }) {
  return (
    <div>
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