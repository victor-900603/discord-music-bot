import axios from 'axios';
import { toast } from './toastHelpler';

const axiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
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


export const setInterceptor = (axiosInstance, navigate) => {
    axiosInstance.interceptors.response.use(
        (response) => {
            const { message } = response.data;
            if (message) {
                toast(message);
            }
            return response;
        },
        (error) => {
            if (error.response) {
                console.error('Response error:', error.response.data);
                const { status } = error.response;
                if (status === 401) {
                    navigate('/error/401', { replace: true });
                } else if (status === 404) {
                    navigate('/error/404', { replace: true });
                } else if (status === 500) {
                    alert('Server error, please try again later.');
                }
            } else if (error.request) {
                console.error('No response received:', error.request);
            } else {
                console.error('Error setting up the request:', error.message);
            }
            const message = error.message;
            if (message) {
                toast(message, 'error');
            }
            return Promise.reject(error); 
        }
    );
}


export default axiosInstance;