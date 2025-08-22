import axiosInstance from "../utils/axiosInstance";

export const removeFromPlaylist = async (index) => {
    try {
        const response = await axiosInstance.delete(`/playlist/?index=${index}`);
        return response.data;
    } catch (error) {
        console.error('Error removing song:', error);
    }
}

export const addToPlaylist = async (id, mode) => {
    try {
        const response = await axiosInstance.post(`/playlist/?id=${id}&mode=${mode}`);
        return response.data;
    } catch (error) {
        console.error('Error AddToPlaylist:', error);
    }
}
