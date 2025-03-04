import axios from "axios";

// Set your backend API base URL
const API_BASE_URL = "http://127.0.0.1:5000"; 

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;