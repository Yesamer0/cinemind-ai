import "./App.css";
import { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import MovieList from "./components/MovieList";

function App() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadPopularMovies() {
      try {
        setLoading(true);

        const response = await fetch("http://127.0.0.1:8000/popular");
        const data = await response.json();

        setMovies(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    loadPopularMovies();
  }, []);

  return (
    <div>
      <h1>🎬 CineMind AI</h1>

      <SearchBar
        setMovies={setMovies}
        setLoading={setLoading}
        setError={setError}
      />

      {loading && <p>Loading movies...</p>}
      {error && <p>{error}</p>}
      <MovieList movies={movies} />
    </div>
  );
}

export default App;