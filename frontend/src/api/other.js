import axiosInstance from "../utils/axiosInstance";

export const searchYouTube = async (keyword) => {
    try {
        const response = await axiosInstance.get(`/search/?keyword=${keyword}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching search results:', error);
    }
}