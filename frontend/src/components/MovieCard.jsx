import { Link } from "react-router-dom";

function MovieCard({ movie }) {

  const posterUrl =
    movie.poster_path &&
    typeof movie.poster_path === "string" &&
    movie.poster_path.startsWith("/")
      ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
      : null;

  const aiScore =
    movie.score !== undefined && movie.score !== null
      ? movie.score
      : movie.similarity !== undefined && movie.similarity !== null
        ? movie.similarity
        : null;

  return (

    <Link
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
          cursor: "pointer",
          height: "100%",
          transition: "transform 0.2s ease, box-shadow 0.2s ease",
          border: "1px solid #333"
        }}

        onMouseEnter={(e) => {
          e.currentTarget.style.transform = "translateY(-6px)";
          e.currentTarget.style.boxShadow =
            "0 10px 25px rgba(0,0,0,0.4)";
        }}

        onMouseLeave={(e) => {
          e.currentTarget.style.transform = "translateY(0)";
          e.currentTarget.style.boxShadow = "none";
        }}
      >

        {posterUrl ? (
          <img
            src={posterUrl}
            alt={movie.title}
            onError={(e) => {
              e.currentTarget.style.display = "none";
              e.currentTarget.nextSibling.style.display = "flex";
            }}
            style={{
              width: "100%",
              height: "320px",
              objectFit: "cover",
              display: "block"
            }}
          />
        ) : null}

        <div
          style={{
            width: "100%",
            height: "320px",
            backgroundColor: "#2a2a2a",
            alignItems: "center",
            justifyContent: "center",
            color: "#888",
            display: posterUrl ? "none" : "flex"
          }}
        >
          No Poster
        </div>

        <div
          style={{
            padding: "18px"
          }}
        >

          <h2
            style={{
              fontSize: "20px",
              margin: "0 0 10px",
              color: "white"
            }}
          >
            {movie.title}
          </h2>

          <p
            style={{
              color: "#aaa",
              fontSize: "14px",
              lineHeight: "1.5",
              height: "65px",
              overflow: "hidden",
              marginBottom: "15px"
            }}
          >
            {movie.overview}
          </p>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center"
            }}
          >

            {aiScore !== null && (
  <strong
    style={{
      color: "#ffd700"
    }}
  >
    🤖 {Number(aiScore).toFixed(2)}
  </strong>
)}

            {movie.rating !== undefined &&
              movie.rating !== null && (
                <strong
                  style={{
                    color: "#fff"
                  }}
                >
                  ⭐ {movie.rating}
                </strong>
              )}

          </div>

        </div>

      </div>
    </Link>
  );
}

export default MovieCard;