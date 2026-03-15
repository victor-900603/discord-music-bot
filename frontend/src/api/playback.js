import axiosInstance from "../utils/axiosInstance";

export const skiptoIndex = async (index) => {
    try {
        const response = await axiosInstance.get(`/playback/skipto/?index=${index}`);
        return response.data;
    } catch (error) {
        console.error('Error skipping to song:', error);
    }
}

export const pause = async () => {
    try {
        const response = await axiosInstance.get('/playback/pause/');
        return response.data;
    } catch (error) {
        console.error('Error pausing playback:', error);
    }
}

export const play = async () => {
    try {
        const response = await axiosInstance.get('/playback/play/');
        return response.data;
    } catch (error) {
        console.error('Error playing playback:', error);
    }
}

export const toggleLoop = async () => {
    try {
        const response = await axiosInstance.get('/playback/loop/');
        return response.data;
    } catch (error) {
        console.error('Error toggling loop:', error);
    }
}

export const toggleShuffle = async () => {
    try {
        const response = await axiosInstance.get('/playback/shuffle/');
        return response.data;
    } catch (error) {
        console.error('Error toggling shuffle:', error);
    }
}

export const setVolume = async (value) => {
    try {
        const response = await axiosInstance.get(`/playback/volume/?value=${value}`);
        return response.data;
    } catch (error) {
        console.error('Error setting volume:', error);
    }
}