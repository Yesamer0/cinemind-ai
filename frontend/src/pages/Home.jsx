import { useEffect, useState } from "react";
import axios from "axios";

import SearchBar from "../components/SearchBar";
import MovieList from "../components/MovieList";
import MovieCard from "../components/MovieCard";

function Home() {
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const [recommendations, setRecommendations] = useState([]);
    const [popularMovies, setPopularMovies] = useState([]);

    // AI Movie Assistant
    const [aiQuery, setAiQuery] = useState("");
    const [aiMovies, setAiMovies] = useState([]);
    const [aiLoading, setAiLoading] = useState(false);
    const [aiError, setAiError] = useState("");
    const [semanticQuery, setSemanticQuery] = useState("");

    useEffect(() => {
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

    async function handleAiRecommend() {
        const query = aiQuery.trim();

        if (!query) {
            setAiError(
                "Please describe what kind of movie you want to watch."
            );
            return;
        }

        setAiLoading(true);
        setAiError("");
        setAiMovies([]);
        setSemanticQuery("");

        try {
            const response = await axios.get(
                "http://127.0.0.1:8000/ai-recommend",
                {
                    params: {
                        query: query
                    }
                }
            );

            setAiMovies(
                response.data.results || []
            );

            setSemanticQuery(
                response.data.semantic_query || ""
            );
        } catch (error) {
            console.error(
                "AI recommendation error:",
                error
            );

            setAiError(
                "AI recommendations could not be loaded."
            );
        } finally {
            setAiLoading(false);
        }
    }

    function handleAiKeyDown(event) {
        if (event.key === "Enter") {
            handleAiRecommend();
        }
    }

    return (
        <main className="home-page">

            {/* HERO */}

            <section className="hero-section">
                <div className="hero-badge">
                    ✦ AI-POWERED MOVIE DISCOVERY
                </div>

                <h1>
                    Find your next
                    <span> favorite movie.</span>
                </h1>

                <p>
                    Search by meaning, discover personalized recommendations
                    and let AI understand exactly what you feel like watching.
                </p>
            </section>


            {/* NORMAL SEARCH */}

            <section className="content-section search-section">
                <SearchBar
                    setMovies={setMovies}
                    setLoading={setLoading}
                    setError={setError}
                />
            </section>


            {loading && (
                <div className="status-message">
                    🔎 Searching movies...
                </div>
            )}


            {error && (
                <div className="status-message error-message">
                    {error}
                </div>
            )}


            {movies.length > 0 && (
                <section className="content-section">
                    <div className="section-heading">
                        <div>
                            <span className="section-label">
                                SEARCH
                            </span>

                            <h2>
                                🔎 AI Search Results
                            </h2>
                        </div>
                    </div>

                    <MovieList movies={movies} />
                </section>
            )}


            {/* AI MOVIE ASSISTANT */}

            <section className="ai-assistant">

                <div className="ai-assistant-header">
                    <div className="ai-icon">
                        ✨
                    </div>

                    <div>
                        <span className="section-label">
                            LOCAL LLAMA AI
                        </span>

                        <h2>
                            AI Movie Assistant
                        </h2>

                        <p>
                            Tell CineMind naturally what you feel like
                            watching. You can write in Turkish or English.
                        </p>
                    </div>
                </div>

                <div className="ai-input-container">

                    <input
                        className="ai-input"
                        type="text"
                        value={aiQuery}
                        onChange={(event) =>
                            setAiQuery(event.target.value)
                        }
                        onKeyDown={handleAiKeyDown}
                        placeholder="Örn: Eğlenceli ama çocukça olmayan romantik bir film istiyorum..."
                    />

                    <button
                        className="ai-button"
                        onClick={handleAiRecommend}
                        disabled={aiLoading}
                    >
                        {aiLoading
                            ? "AI is thinking..."
                            : "✨ AI Recommend"}
                    </button>

                </div>


                {aiError && (
                    <div className="status-message error-message">
                        {aiError}
                    </div>
                )}


                {semanticQuery && (
                    <div className="ai-understood">
                        <span>
                            🧠 Llama understood
                        </span>

                        <p>
                            {semanticQuery}
                        </p>
                    </div>
                )}

            </section>


            {/* AI RESULTS */}

            {aiMovies.length > 0 && (
                <section className="content-section">

                    <div className="section-heading">
                        <div>
                            <span className="section-label">
                                LLAMA + FAISS
                            </span>

                            <h2>
                                ✨ AI Recommendations
                            </h2>
                        </div>
                    </div>

                    <div className="movie-grid">
                        {aiMovies.map((movie) => (
                            <MovieCard
                                key={movie.id}
                                movie={movie}
                            />
                        ))}
                    </div>

                </section>
            )}


            {/* PERSONALIZED RECOMMENDATIONS */}

            {recommendations.length > 0 && (
                <section className="content-section">

                    <div className="section-heading">
                        <div>
                            <span className="section-label">
                                PERSONALIZED
                            </span>

                            <h2>
                                🎯 Recommended for You
                            </h2>
                        </div>
                    </div>

                    <div className="movie-grid">
                        {recommendations.map((movie) => (
                            <MovieCard
                                key={movie.id}
                                movie={movie}
                            />
                        ))}
                    </div>

                </section>
            )}


            {/* POPULAR */}

            {popularMovies.length > 0 && (
                <section className="content-section">

                    <div className="section-heading">
                        <div>
                            <span className="section-label">
                                TRENDING
                            </span>

                            <h2>
                                🔥 Popular Movies
                            </h2>
                        </div>
                    </div>

                    <div className="movie-grid">
                        {popularMovies.map((movie) => (
                            <MovieCard
                                key={movie.id}
                                movie={movie}
                            />
                        ))}
                    </div>

                </section>
            )}

        </main>
    );
}

export default Home;