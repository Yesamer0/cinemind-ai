import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function MovieDetail() {

    const { id } = useParams();

    const [movie, setMovie] = useState(null);

    useEffect(() => {

        async function fetchMovie() {

            try {

                const response = await axios.get(
                    `http://127.0.0.1:8000/movie/${id}`
                );

                setMovie(response.data);

            } catch (error) {

    console.error("HATA:", error);

    if (error.response) {
        console.log("Status:", error.response.status);
        console.log("Data:", error.response.data);
    }

}
        }

        fetchMovie();

    }, [id]);

    if (!movie) {

        return <h2>Loading...</h2>;

    }

    return (
    <div
        style={{
            maxWidth: "800px",
            margin: "40px auto",
            padding: "20px"
        }}
    >
        <h1>{movie.title}</h1>

        <p>
            ⭐ <strong>Rating:</strong> {movie.rating}
        </p>

        <p>
            🎭 <strong>Genres:</strong> {movie.genres}
        </p>

        <p>
            📅 <strong>Release Date:</strong> {movie.release_date}
        </p>

        <hr />

        <h3>Overview</h3>

        <p>{movie.overview}</p>

    </div>
);

}

export default MovieDetail;