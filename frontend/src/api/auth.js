import axiosInstance from "../utils/axiosInstance";

export const auth = async () => {
    try {
        const resp = await axiosInstance.get('/auth/set/');
        return resp.data;
    } catch (e) {
        console.error('Error set auth:', e);
    }
}

export const getAuth = async () => {
    try {
        const response = await axiosInstance.get('/auth/');
        return response.data
    } catch (error) {
        console.error('Error get auth:', error);
    }
}