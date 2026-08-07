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
        <div
            style={{
                minHeight: "100vh",
                padding: "40px 60px",
                backgroundColor: "#111",
                color: "white"
            }}
        >
            <h1
                style={{
                    textAlign: "center",
                    fontSize: "42px",
                    marginBottom: "10px"
                }}
            >
                🎬 CineMind AI
            </h1>

            <p
                style={{
                    textAlign: "center",
                    color: "#aaa",
                    marginBottom: "35px"
                }}
            >
                Discover movies with AI-powered semantic search
            </p>

            <SearchBar
                setMovies={setMovies}
                setLoading={setLoading}
                setError={setError}
            />

            {loading && (
                <p style={{ textAlign: "center", marginTop: "30px" }}>
                    🔎 Searching movies...
                </p>
            )}

            {error && (
                <p
                    style={{
                        textAlign: "center",
                        color: "#ff6b6b",
                        marginTop: "30px"
                    }}
                >
                    {error}
                </p>
            )}

            <MovieList movies={movies} />
        </div>
    );
}

export default Home;