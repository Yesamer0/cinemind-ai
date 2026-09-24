import axios from "axios";
import { useState } from "react";

function SearchBar({ setMovies, setLoading, setError }) {
  const [searchText, setSearchText] = useState("");

  async function handleSearch() {
    const query = searchText.trim();

    if (!query) {
      setError(
        "Please enter what kind of movie you are looking for."
      );
      setMovies([]);
      return;
    }

    try {
      setError("");
      setLoading(true);

      const response = await axios.get(
        "http://127.0.0.1:8000/search",
        {
          params: {
            query: query
          }
        }
      );

      setMovies(response.data.results || []);

    } catch (error) {
      setError("Something went wrong.");
      console.error(error);
      setMovies([]);

    } finally {
      setLoading(false);
    }
  }


  async function handleKeywordSearch() {
    const query = searchText.trim();

    if (!query) {
      setError("Please enter a keyword.");
      setMovies([]);
      return;
    }

    try {
      setError("");
      setLoading(true);

      const response = await axios.get(
        "http://127.0.0.1:8000/keyword-recommendations",
        {
          params: {
            query: query
          }
        }
      );

      setMovies(response.data.results || []);

    } catch (error) {
      setError("Keyword recommendation failed.");
      console.error(error);
      setMovies([]);

    } finally {
      setLoading(false);
    }
  }


  function handleKeyDown(event) {
    if (event.key === "Enter") {
      handleSearch();
    }
  }


  return (
    <div className="search-box">

      <div className="search-box-header">
        <span className="search-box-icon">
          🔎
        </span>

        <div>
          <span className="section-label">
            SMART SEARCH
          </span>

          <h2>Explore Movies</h2>
        </div>
      </div>


      <div className="search-controls">

        <input
          className="movie-search-input"
          type="text"
          placeholder="Describe a movie, story, mood or theme..."
          value={searchText}
          onChange={(e) =>
            setSearchText(e.target.value)
          }
          onKeyDown={handleKeyDown}
        />


        <div className="search-buttons">

          <button
            className="search-button semantic-button"
            onClick={handleSearch}
          >
            🤖 Semantic Search
          </button>

          <button
            className="search-button keyword-button"
            onClick={handleKeywordSearch}
          >
            🔤 Keyword Search
          </button>

        </div>

      </div>

      <p className="search-help">
        Search by meaning with AI or use traditional keyword matching.
      </p>

    </div>
  );
}

export default SearchBar;