import React, { useState, useEffect, useContext } from 'react'
import { useParams } from 'react-router-dom';
import Modal from '../components/modal';
import * as Icon from 'react-feather';
import '../styles/page.scss'

import { getFavorites, addToFavorite } from '../api/favorite';
import { addToPlaylist } from '../api/playlist';
import { searchYouTube } from '../api/other';

const AddToFavoriteModal = ({isOpen, onClose, song}) => {
    if (!isOpen) return null;

    const [favorites, setFavorites] = useState([]);
    const [selectedFavoriteId, setSelectedFavoriteId] = useState(null);

    useEffect(() => {
        const fetchFavorites = async () => {
            const data = await getFavorites();
            if (data) {
                setFavorites(data.result);
                setSelectedFavoriteId(data.result[0]?._id || null);
            }
        }
        fetchFavorites();
    }, []);


    const handleAddToFavorite = async () => {
        await addToFavorite(song, selectedFavoriteId);
        onClose();
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
                <div className="action play-action" onClick={() => addToPlaylist(videoId, 'song')}>
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
            const data = await searchYouTube(keyword);
            if (data) {
                setSearchResults(data);
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