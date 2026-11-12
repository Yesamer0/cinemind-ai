import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
});

api.interceptors.response.use(undefined, (error) => {
  const token = localStorage.getItem("token");
  if (
    error.response?.status === 401 &&
    token &&
    error.config?.headers?.get("Authorization") === `Bearer ${token}`
  ) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.assign("/login");
  }
  return Promise.reject(error);
});

const posterBaseUrl = import.meta.env.VITE_TMDB_IMAGE_BASE_URL || "https://image.tmdb.org/t/p/w500";

export function posterUrl(path) {
  return `${posterBaseUrl.replace(/\/$/, "")}/${path.replace(/^\//, "")}`;
}

export default api;
