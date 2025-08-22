import axiosInstance from "../utils/axiosInstance";

export const addToFavorite = async (song, favorite_Id) => {
    try {
        const response = await axiosInstance.post(`/favorites/${favorite_Id}/song/`, {
            id: song.videoId,
            title: song.title,
            channel: song.channel,
            thumbnail: song.thumbnail
        })
        return response.data;
    } catch (error) {
        console.error('Error AddToFavorite:', error);
    }
}

export const getFavoriteSongs = async (id) => {
    try {
        const resp = await axiosInstance.get('/favorites/' + id + '/songs/');
        return resp.data;
    } catch (error) {
        console.error('Error fetching favorite songs:', error);
    }
}

export const deleteFromFavorite = async (favorite_id, song_id) => {
    try {
        const response = await axiosInstance.delete(`/favorites/${favorite_id}/song/${song_id}/`);
        return response.data;
    } catch (error) {
        console.error('Error deleting favorite song:', error);
    }
}

export const addFavorite = async (name) => {
    try {
        const response = await axiosInstance.post('/favorites/?name=' + name);
        return response.data;
    } catch (error) {
        console.error('Error adding favorite:', error);
    }
}

export const getFavorites = async () => {
    try {
        const resp = await axiosInstance.get('/favorites/');
        return resp.data;
    } catch (error) {
        console.error('Error fetching favorites:', error);
    }
}

export const deleteFavorite = async (id) => {
    try {
        const response = await axiosInstance.delete(`/favorites/${id}/`);
        return response.data;
    } catch (error) {
        console.error('Error delete favorite:', error);
    }
}