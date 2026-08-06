import { useState, useEffect } from "react";
import SearchBar from "../components/SearchBar";
import MovieList from "../components/MovieList";

function Home() {

    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {

        console.log("Home Page");

    }, []);

    return (
        <div>

            <h1>🎬 CineMind AI</h1>

            <SearchBar
                setMovies={setMovies}
                setLoading={setLoading}
                setError={setError}
            />

            {loading && <p>Loading...</p>}

            {error && <p>{error}</p>}

            <MovieList movies={movies} />

        </div>
    );

}

export default Home;