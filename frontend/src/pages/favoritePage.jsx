import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";
import * as Icon from 'react-feather';

import { deleteFromFavorite, deleteFavorite, getFavoriteSongs } from "../api/favorite";
import { addToPlaylist } from "../api/playlist";
import Modal from "../components/modal";

const FavoriteSongItem = ({song, onDeleted}) => {
    const params = useParams();
    const favorite_id = params.id;

    const handleAddToPlaylist = async (id) => {
        await addToPlaylist(id, 'song');
    }

    const handleDeleteFavoriteSong = async (id) => {
        await deleteFromFavorite(favorite_id, id);
        onDeleted();
    }

    return (
        <li className="favorite-song-item">
            <div className='favorite-song-btn' onClick={() => handleAddToPlaylist(song.id)} >
                <div className="favorite-song-cover">
                    <img src={song.thumbnail} alt="" />
                    <div className="favorite-song-overlay">
                        <Icon.PlusCircle />
                    </div>
                </div>
                <div className='favorite-song-info'>
                    <h2 title={song.title}>{song.title}</h2>
                    <p>{song.channel}</p>
                </div>
            </div>
            <div className="favorite-song-delete-btn" onClick={() => handleDeleteFavoriteSong(song.id)}>
                <Icon.Trash2 />
            </div>
        </li>
    )
}

const FavoriteSongsList = ({songs, onDeleted}) => {
    return (
        <ul className="favorite-songs-list">
            {songs.map((song) => (
                <FavoriteSongItem key={song.id} song={song} onDeleted={onDeleted} />
            ))}
        </ul>
    )
}

const FavoriteController = ({id}) => {
    const [isOpen, setIsOpen] = useState(false);
    const navigate = useNavigate();

    const handleDeleteFavorite = async () => {
        await deleteFavorite(id);
        navigate('/');
    }
    
    return (
        <div className="favorite-controller" >
            <div className="favorite-controller-btn play-btn" onClick={() => addToPlaylist(id, 'favorite')}>
                <Icon.PlusCircle />
                <span>播放</span>
            </div>
            <div className="favorite-controller-btn delete-btn" onClick={() => setIsOpen(true)}>
                <Icon.Trash2 />
                <span>刪除</span>
            </div>
            <Modal isOpen={isOpen} onClose={() => setIsOpen(false)}>
                <h2 className="modal-title">確認刪除</h2>
                <input className="modal-btn" type="button" value={"刪除"} onClick={() => handleDeleteFavorite()} />
            </Modal>
        </div>
    )
}

const FavoritePage = () => {
    const {id} = useParams();
    const [name, setName] = useState("");
    const [songs, setSongs] = useState([]);

    const fetchSongs = useCallback(async () => {
        const data = await getFavoriteSongs(id);
        if (data) {
            setName(data.result.name);
            setSongs(data.result.songs);
        }
    }, [id]);

    useEffect(() => {
        fetchSongs();
    }, [fetchSongs]);

    return (
        <div className="page favorite-page">
            <div className="favorite-page-header">
                <h1>{name}</h1>
                <FavoriteController id={id} />
            </div>
            <FavoriteSongsList songs={songs} onDeleted={fetchSongs} />
        </div>
    )
}

export default FavoritePage;