import axios from "axios";
import { useState } from "react";

function SearchBar({ setMovies, setLoading, setError }) {
  const [searchText, setSearchText] = useState("");

  async function handleSearch() {
    try {
      setError("");
      setLoading(true);

      const response = await axios.get(
        `http://127.0.0.1:8000/search?query=${searchText}`
      );

      setMovies(response.data.results);

    } catch (error) {
      setError("Something went wrong.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <input
        type="text"
        placeholder="Search for a movie..."
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
      />

      <button onClick={handleSearch}>
        Search
      </button>
    </div>
  );
}

export default SearchBar;