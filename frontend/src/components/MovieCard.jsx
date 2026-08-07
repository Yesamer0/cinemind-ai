import { Link } from "react-router-dom";

function MovieCard({ movie }) {
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
          e.currentTarget.style.boxShadow = "0 10px 25px rgba(0,0,0,0.4)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = "translateY(0)";
          e.currentTarget.style.boxShadow = "none";
        }}
      >

        {movie.poster_path ? (
          <img
            src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
            alt={movie.title}
            style={{
              width: "100%",
              height: "320px",
              objectFit: "cover",
              display: "block"
            }}
          />
        ) : (
          <div
            style={{
              width: "100%",
              height: "320px",
              backgroundColor: "#2a2a2a",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#888"
            }}
          >
            No Poster
          </div>
        )}

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
            <strong
              style={{
                color: "#ffd700"
              }}
            >
              🤖 {movie.score}
            </strong>

            {movie.rating !== undefined && (
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