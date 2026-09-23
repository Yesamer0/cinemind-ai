import axios from "axios";
import { useState } from "react";

function SearchBar({ setMovies, setLoading, setError }) {
  const [searchText, setSearchText] = useState("");

  async function handleSearch() {

    const query = searchText.trim();

    if (!query) {
      setError("Please enter what kind of movie you are looking for.");
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
    <div>
      <input
        type="text"
        placeholder="Describe the movie you want..."
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
        onKeyDown={handleKeyDown}
      />

      <button onClick={handleSearch}>
  🤖 Semantic Search
</button>

<button onClick={handleKeywordSearch}>
  🔤 Keyword Search
</button>
    </div>
  );
}

export default SearchBar;