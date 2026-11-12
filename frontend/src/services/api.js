import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
});

const posterBaseUrl = import.meta.env.VITE_TMDB_IMAGE_BASE_URL || "https://image.tmdb.org/t/p/w500";

export function posterUrl(path) {
  return `${posterBaseUrl.replace(/\/$/, "")}/${path.replace(/^\//, "")}`;
}

export default api;
