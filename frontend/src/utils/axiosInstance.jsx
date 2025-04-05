import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/', 
    timeout: 10000, 
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
});


axiosInstance.interceptors.request.use(
    (config) => {
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

axiosInstance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response) {
            console.error('Response error:', error.response.data);
            if (error.response.status === 401) {
                console.log();
            }
        } else if (error.request) {
            console.error('No response received:', error.request);
        } else {
            console.error('Error setting up the request:', error.message);
        }
        return Promise.reject(error); 
    }
);
export default axiosInstance;