import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

function MovieDetail() {

    const { id } = useParams();

    const [movie, setMovie] = useState(null);
    const [error, setError] = useState("");
    const [isFavorite, setIsFavorite] = useState(false);
    const [favoriteLoading, setFavoriteLoading] = useState(false);
    const [userRating, setUserRating] = useState(null);
    const [ratingLoading, setRatingLoading] = useState(false);
    useEffect(() => {

        async function loadMovie() {

            try {

                const response = await axios.get(
                    `http://127.0.0.1:8000/movie/${id}`
                );

                setMovie(response.data);

                const token = localStorage.getItem("token");

                if (token) {

                    const favoritesResponse = await axios.get(
                        "http://127.0.0.1:8000/favorites",
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );

                    const favoriteIds =
                        favoritesResponse.data.map(
                            (favorite) => favorite.movie_id
                        );

                    setIsFavorite(
                        favoriteIds.includes(Number(id))
                    );

                    const ratingResponse = await axios.get(
    `http://127.0.0.1:8000/ratings/${id}`,
    {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }
);

setUserRating(ratingResponse.data.rating);




                }

            } catch (error) {

                console.error(error);

                setError(
                    "Movie could not be loaded."
                );
            }
        }

        loadMovie();

    }, [id]);


    async function handleFavorite() {

        const token = localStorage.getItem("token");

        if (!token) {

            alert("Please login first.");

            return;
        }

        try {

            setFavoriteLoading(true);

            if (isFavorite) {

                await axios.delete(
                    `http://127.0.0.1:8000/favorites/${id}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                setIsFavorite(false);

            } else {

                await axios.post(
                    `http://127.0.0.1:8000/favorites/${id}`,
                    null,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                setIsFavorite(true);
            }

        } catch (error) {

            console.error(error);

            alert(
                error.response?.data?.detail ||
                "Something went wrong."
            );

        } finally {

            setFavoriteLoading(false);
        }
    }
    async function handleRating(rating) {

    const token = localStorage.getItem("token");

    if (!token) {
        alert("Please login first.");
        return;
    }

    try {

        setRatingLoading(true);

        await axios.post(
            `http://127.0.0.1:8000/ratings/${id}?rating=${rating}`,
            null,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        setUserRating(rating);

    } catch (error) {

        console.error(error);

        alert(
            error.response?.data?.detail ||
            "Could not save rating."
        );

    } finally {

        setRatingLoading(false);
    }
}

    if (error) {

        return (
            <div
                style={{
                    minHeight: "100vh",
                    backgroundColor: "#111",
                    color: "white",
                    padding: "40px",
                    textAlign: "center"
                }}
            >

                <h2>{error}</h2>

                <Link to="/">
                    <button>
                        ← Back to Home
                    </button>
                </Link>

            </div>
        );
    }


    if (!movie) {

        return (
            <div
                style={{
                    minHeight: "100vh",
                    backgroundColor: "#111",
                    color: "white",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center"
                }}
            >

                <h2>Loading movie...</h2>

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

            <Link
                to="/"
                style={{
                    textDecoration: "none"
                }}
            >

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


            <div
                style={{
                    maxWidth: "1000px",
                    margin: "0 auto",
                    display: "flex",
                    gap: "40px",
                    alignItems: "flex-start",
                    flexWrap: "wrap"
                }}
            >

                {movie.poster_path && (

                    <img
                        src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                        alt={movie.title}
                        style={{
                            width: "320px",
                            borderRadius: "16px",
                            boxShadow:
                                "0 10px 30px rgba(0,0,0,0.5)"
                        }}
                    />

                )}


                <div
                    style={{
                        flex: 1,
                        minWidth: "300px"
                    }}
                >

                    <h1
                        style={{
                            fontSize: "42px",
                            marginTop: 0,
                            marginBottom: "20px"
                        }}
                    >
                        {movie.title}
                    </h1>


                    <div style={{ marginBottom: "20px" }}>

    <p style={{ marginBottom: "8px" }}>
        Your Rating:
    </p>

    <div>
        {[1, 2, 3, 4, 5].map((star) => (
            <button
                key={star}
                onClick={() => handleRating(star)}
                disabled={ratingLoading}
                style={{
                    background: "none",
                    border: "none",
                    fontSize: "30px",
                    cursor: "pointer",
                    padding: "2px"
                }}
            >
                {userRating >= star ? "⭐" : "☆"}
            </button>
        ))}
    </div>

</div>


                    <button
                        onClick={handleFavorite}
                        disabled={favoriteLoading}
                        style={{
                            backgroundColor:
                                isFavorite
                                    ? "#e63946"
                                    : "#333",

                            color: "white",

                            border: "none",

                            padding: "12px 20px",

                            borderRadius: "8px",

                            cursor: favoriteLoading
                                ? "default"
                                : "pointer",

                            marginBottom: "25px",

                            fontSize: "16px"
                        }}
                    >

                        {favoriteLoading
                            ? "Saving..."
                            : isFavorite
                                ? "❤️ Remove from Favorites"
                                : "🤍 Add to Favorites"
                        }

                    </button>


                    <div
                        style={{
                            display: "flex",
                            gap: "20px",
                            flexWrap: "wrap",
                            marginBottom: "25px"
                        }}
                    >

                        <span>
                            ⭐ Rating: {movie.rating}
                        </span>

                        <span>
                            🎭 {movie.genres}
                        </span>

                        <span>
                            📅 {movie.release_date}
                        </span>

                    </div>


                    <h2>Overview</h2>

                    <p
                        style={{
                            color: "#ccc",
                            lineHeight: "1.8",
                            fontSize: "17px"
                        }}
                    >
                        {movie.overview}
                    </p>

                </div>

            </div>

        </div>
    );
}

export default MovieDetail;