import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import * as Icon from 'react-feather';

import { deleteFromFavorite, deleteFavorite, getFavoriteSongs } from "../api/favorite";
import { addToPlaylist } from "../api/playlist";
import Modal from "../components/modal";

const FavoriteSongItem = ({song}) => {
    const params = useParams();
    const favorite_id = params.id;

    const handleAddToPlaylist = async (id) => {
        await addToPlaylist(id, 'song');
    }

    const handleDeleteFavoriteSong = async (id) => {
        await deleteFromFavorite(favorite_id, id);
        window.location.reload();
    }

    return (
        <li className="favorite-song-item">
            <div className='favorite-song-btn' onClick={handleAddToPlaylist.bind(null, song.id)} >
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
            <div className="favorite-song-delete-btn" onClick={handleDeleteFavoriteSong.bind(null, song.id)}>
                <Icon.Trash2 />
            </div>
        </li>
    )
}

const FavoriteSongsList = ({songs}) => {
    return (
        <ul className="favorite-songs-list">
            {songs.map((song, index) => {
                return (
                    <FavoriteSongItem song={song} />
                )
            })}
        </ul>
    )
}

const FavoriteController = ({id}) => {
    const [isOpen, setIsOpen] = useState(false);

    const handleDeleteFavorite = async () => {
        await deleteFavorite(id);
        window.location.href = '/';
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

    useEffect(() => {
        const fetchSongs = async () => {
            const data = await getFavoriteSongs(id);
            if (data) {
                setName(data.result.name);
                setSongs(data.result.songs);
            }
        }
        fetchSongs();
    }, []);

    return (
        <div className="page favorite-page">
            <div className="favorite-page-header">
                <h1>{name}</h1>
                <FavoriteController id={id} />

            </div>
            <FavoriteSongsList songs={songs} />
        </div>
    )
}

export default FavoritePage;