import axios from "axios";


const baseUrl = `${window.location.origin}/api/v1/`;

export const simpleRequest = axios.create({
    baseURL: baseUrl,
    headers: {
        "Content-type": "application/json",
    },
});

const axiosInstance = axios.create({
  baseURL: baseUrl,
  timeout: 5000,
  headers: {
  'Authorization': localStorage.getItem('jwtToken') ? "JWT " +
      JSON.parse(localStorage.getItem('jwtToken')).access : null,
    "Content-Type": "application/json",
    accept: "application/json",
  },
});

axiosInstance.interceptors.response.use(
    response => response,
    error => {
        const originalRequest = error.config;
        // Prevent infinite loops
        if (error.response.status === 401 && originalRequest.url === baseUrl + 'login/refresh/') {
            localStorage.clear();
            window.location.replace("/login");
        }
        if (error.response.status === 401 &&
            error.response.statusText === "Unauthorized")
            {
                const refreshToken = JSON.parse(localStorage.getItem('jwtToken')).access;
                if (refreshToken){
                    const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));
                    // exp date in token is expressed in seconds, while now() returns milliseconds:
                    const now = Math.ceil(Date.now() / 1000);
                    if (tokenParts.exp > now) {
                        return axiosInstance
                            .post('/login/refresh/', {refresh: refreshToken})
                                .then((response) => {
                                    localStorage.setItem('jwtToken', response.data);
                                    axiosInstance.defaults.headers['Authorization'] = "JWT " + response.data.access;
                                    originalRequest.headers['Authorization'] = "JWT " + response.data.access;
                                    return axiosInstance(originalRequest);
                                })
                                .catch(err => {
                                    console.log(err)
                                    localStorage.clear();
                                    window.location.replace("/login");
                                });
                    }
                }
        }
      // specific error handling done elsewhere
      localStorage.clear();
      window.location.replace("/login");
  }
);

export default axiosInstance;
