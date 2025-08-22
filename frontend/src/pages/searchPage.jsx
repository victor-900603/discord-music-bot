import React, { useState, useEffect, useContext } from 'react'
import { useParams } from 'react-router-dom';
import Modal from '../components/modal';
import * as Icon from 'react-feather';
import '../styles/page.scss'
import axiosInstance from '../utils/axiosInstance';


const AddToFavoriteModal = ({isOpen, onClose, song}) => {
    if (!isOpen) return null;

    const [favorites, setFavorites] = useState([]);
    const [selectedFavoriteId, setSelectedFavoriteId] = useState(null);

    useEffect(() => {
        const fetchFavorites = async () => {
            try {
                const resp = await axiosInstance.get('/favorites');
                setFavorites(resp.data.result);
                setSelectedFavoriteId(resp.data.result[0]?._id || null);
            } catch (error) {
                console.error('Error fetching favorites:', error);
            }
        }
        fetchFavorites();
    }, []);


    const handleAddToFavorite = async () => {
        try {
            const response = await axiosInstance.post(`/favorites/${selectedFavoriteId}/song`,{
                id: song.videoId,
                title: song.title,
                channel: song.channel,
                thumbnail: song.thumbnail
            })
            onClose();
        } catch (error) {
            console.error('Error AddToFavorite:', error);
            
        }
    }
    return (
        <Modal isOpen={isOpen} onClose={onClose}>
            <h2 className="modal-title">新增至收藏</h2>
            <ul className="favorite-list">
                {favorites.map((favorite, index) => (
                    <li className={(selectedFavoriteId==favorite._id)? 'favorite selected': 'favorite'} key={favorite._id} onClick={() => {setSelectedFavoriteId(favorite._id)}}>
                        {favorite.name}
                    </li>
                ))}
                <input className="modal-btn" type="button" value={"新增"} onClick={() => handleAddToFavorite()} disabled={!selectedFavoriteId} />
            </ul>
        </Modal>
    )

}

const SearchItem = ({ song }) => {
    const { videoId, title, thumbnail, length, channel } = song;
    const [isOpen, setIsOpen] = useState(false);

    const handleAddToPlaylist = async (id) => {
        try {
            const response = await axiosInstance.post('/playlist?id=' + id);
            console.log(response.data);
        } catch (error) {
            console.error('Error AddToPlaylist:', error);
        }
    }

    return (
        <li className='search-item'>
            <div className='search-item-content'>
                <img src={thumbnail} alt={title} />
                <div className='search-item-info'>
                    <h2>{title}</h2>
                    <p>{channel}</p>
                    <p>{length}</p>
                </div>
            </div>
            <div className='search-item-action'>
                <div className="action play-action" onClick={() => handleAddToPlaylist(videoId)}>
                    <Icon.PlusCircle />
                </div>
                <div className="action favorite-action" onClick={() => setIsOpen(true)}>
                    <Icon.Heart />
                </div>
            </div>
            <AddToFavoriteModal isOpen={isOpen} onClose={() => setIsOpen(false)} song={song} />
        </li>
    )
}
const SearchList = ({ result }) => {
    return (
        <ul className='search-list'>
            {result.map((song, index) => (
                <SearchItem key={index} song={song} />
            ))}
        </ul>
    )
}

const SearchPage = () => {
    const { keyword } = useParams();

    const [searchResults, setSearchResults] = useState([]);

    useEffect(() => {
        const fetchSearchResults = async () => {
            try {
                const response = await axiosInstance.get(`/search?keyword=${keyword}`);
                setSearchResults(response.data);
                console.log(response.data);
            } catch (error) {
                console.error('Error fetching search results:', error);
            }
        };
        fetchSearchResults();
    }, [keyword]);

    return (
        <div className="page search-page">
            <h1>{keyword}</h1>
            <SearchList result={searchResults} />
        </div>
    )
}

export default SearchPage;