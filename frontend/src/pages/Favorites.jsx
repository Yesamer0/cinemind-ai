import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

function Favorites() {

    const [favorites, setFavorites] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        async function loadFavorites() {

            const token = localStorage.getItem("token");

            if (!token) {
                setError("Please login to see your favorites.");
                setLoading(false);
                return;
            }

            try {

                // Get favorite movie IDs from backend
                const response = await axios.get(
                    "http://127.0.0.1:8000/favorites",
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                const favoriteIds = response.data.map(
                    (favorite) => favorite.movie_id
                );

                if (favoriteIds.length === 0) {
                    setFavorites([]);
                    setLoading(false);
                    return;
                }

                // Get movie details
                const movieRequests = favoriteIds.map((id) =>
                    axios.get(
                        `http://127.0.0.1:8000/movie/${id}`
                    )
                );

                const movieResponses =
                    await Promise.all(movieRequests);

                setFavorites(
                    movieResponses.map(
                        (response) => response.data
                    )
                );

            } catch (error) {

                console.error(error);

                setError(
                    error.response?.data?.detail ||
                    "Could not load favorites."
                );

            } finally {

                setLoading(false);

            }
        }

        loadFavorites();

    }, []);


    if (loading) {

        return (
            <div
                style={{
                    minHeight: "100vh",
                    backgroundColor: "#111",
                    color: "white",
                    textAlign: "center",
                    padding: "50px"
                }}
            >
                <h2>Loading favorites...</h2>
            </div>
        );
    }


    if (error) {

        return (
            <div
                style={{
                    minHeight: "100vh",
                    backgroundColor: "#111",
                    color: "white",
                    textAlign: "center",
                    padding: "50px"
                }}
            >

                <h2>{error}</h2>

                <Link to="/login">
                    <button
                        style={{
                            backgroundColor: "#333",
                            color: "white",
                            border: "none",
                            padding: "10px 18px",
                            borderRadius: "8px",
                            cursor: "pointer"
                        }}
                    >
                        Go to Login
                    </button>
                </Link>

            </div>
        );
    }


    return (

        <div
            style={{
                minHeight: "100vh",
                backgroundColor: "#111",
                color: "white",
                padding: "40px 60px"
            }}
        >

            <Link to="/">
                <button
                    style={{
                        backgroundColor: "#333",
                        color: "white",
                        border: "none",
                        padding: "10px 18px",
                        borderRadius: "8px",
                        cursor: "pointer",
                        marginBottom: "30px"
                    }}
                >
                    ← Back to Home
                </button>
            </Link>


            <h1>❤️ My Favorites</h1>


            {favorites.length === 0 ? (

                <p style={{ color: "#aaa" }}>
                    You haven't added any favorite movies yet.
                </p>

            ) : (

                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "repeat(auto-fit, minmax(220px, 1fr))",
                        gap: "25px",
                        marginTop: "30px"
                    }}
                >

                    {favorites.map((movie) => (

                        <Link
                            key={movie.id}
                            to={`/movie/${movie.id}`}
                            style={{
                                textDecoration: "none",
                                color: "inherit"
                            }}
                        >

                            <div
                                style={{
                                    backgroundColor: "#1c1c1c",
                                    borderRadius: "16px",
                                    overflow: "hidden",
                                    border: "1px solid #333"
                                }}
                            >

                                {movie.poster_path && (

                                    <img
                                        src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                                        alt={movie.title}
                                        style={{
                                            width: "100%",
                                            height: "320px",
                                            objectFit: "cover"
                                        }}
                                    />

                                )}


                                <div
                                    style={{
                                        padding: "15px"
                                    }}
                                >

                                    <h2>
                                        {movie.title}
                                    </h2>

                                    <p
                                        style={{
                                            color: "#aaa"
                                        }}
                                    >
                                        ⭐ {movie.rating}
                                    </p>

                                    <p
                                        style={{
                                            color: "#aaa"
                                        }}
                                    >
                                        🎭 {movie.genres}
                                    </p>

                                    <p
                                        style={{
                                            color: "#aaa"
                                        }}
                                    >
                                        📅 {movie.release_date}
                                    </p>

                                </div>

                            </div>

                        </Link>

                    ))}

                </div>

            )}

        </div>
    );
}

export default Favorites;