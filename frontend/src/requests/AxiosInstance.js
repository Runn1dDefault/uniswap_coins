import axios from "axios";


const baseUrl = `${window.location.origin}/api/v1/`;

export const axiosInstance = axios.create({
  baseURL: baseUrl,
  headers: {
    "Content-type": "application/json",
  },
});
