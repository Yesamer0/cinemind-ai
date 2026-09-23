import { useState, useEffect } from "react";
import SearchBar from "../components/SearchBar";
import MovieList from "../components/MovieList";
import axios from "axios";
import MovieCard from "../components/MovieCard";

function Home() {
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [recommendations, setRecommendations] = useState([]);
    const [popularMovies, setPopularMovies] = useState([]);

    useEffect(() => {
        console.log("Home Page");


        async function loadPopularMovies() {
    try {
        const response = await axios.get(
            "http://127.0.0.1:8000/popular?limit=10"
        );

        setPopularMovies(response.data);

    } catch (error) {
        console.error(
            "Could not load popular movies:",
            error
        );

        setPopularMovies([]);
    }
}

        async function loadRecommendations() {
            const token = localStorage.getItem("token");

            // Kullanıcı giriş yapmamışsa öneri istemiyoruz
            if (!token) {
                setRecommendations([]);
                return;
            }

            try {
                const response = await axios.get(
                    "http://127.0.0.1:8000/recommendations",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                setRecommendations(
                    response.data.results || []
                );

            } catch (error) {
                console.error(
                    "Could not load recommendations:",
                    error
                );

                setRecommendations([]);
            }
        }

        
        
        
        
        
        loadRecommendations();
        loadPopularMovies();
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


            {/* SEARCH */}

            <SearchBar
                setMovies={setMovies}
                setLoading={setLoading}
                setError={setError}
            />

            {/* SEARCH LOADING */}

{loading && (
    <p
        style={{
            textAlign: "center",
            marginTop: "30px"
        }}
    >
        🔎 Searching movies...
    </p>
)}

{/* ERROR */}

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

{/* SEARCH RESULTS */}

{movies.length > 0 && (
    <div
        style={{
            marginTop: "40px",
            marginBottom: "40px"
        }}
    >
        <h2>
            🔎 AI Search Results
        </h2>

        <MovieList movies={movies} />
    </div>
)}


            {/* RECOMMENDATIONS */}

            {recommendations.length > 0 && (
    <div
        style={{
            marginTop: "40px",
            marginBottom: "40px"
        }}
    >
        <h2 style={{ marginBottom: "20px" }}>
            🎯 Recommended for You
        </h2>

        <div
            style={{
                display: "grid",
                gridTemplateColumns:
                    "repeat(auto-fit, minmax(220px, 1fr))",
                gap: "20px"
            }}
        >
            {recommendations.map((movie) => (
                <MovieCard
                    key={movie.id}
                    movie={movie}
                />
            ))}
        </div>
    </div>
)}          
            {/* POPULAR MOVIES */}

{popularMovies.length > 0 && (
    <div
        style={{
            marginTop: "40px",
            marginBottom: "40px"
        }}
    >
        <h2
            style={{
                marginBottom: "20px"
            }}
        >
            🔥 Popular Movies
        </h2>

        <div
            style={{
                display: "grid",
                gridTemplateColumns:
                    "repeat(auto-fit, minmax(220px, 1fr))",
                gap: "20px"
            }}
        >
            {popularMovies.map((movie) => (
                <MovieCard
                    key={movie.id}
                    movie={movie}
                />
            ))}
        </div>
    </div>
)}

            


            
        </div>
    );
}

export default Home;