import axios from "axios";

// Set your backend API base URL
const API_BASE_URL = "https://your-backend-api.com"; 

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;