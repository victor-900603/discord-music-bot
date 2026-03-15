import React, {useState, useEffect, useCallback} from "react";
import * as Icon from 'react-feather';
import '../styles/page.scss'

import { addFavorite, getFavorites } from "../api/favorite";
import { addToPlaylist } from "../api/playlist";
import Modal from "../components/modal";


const AddFavoriteModal = ({isOpen, onClose, onAdded}) => {
    const [name, setName] = useState("");
    const handleAddFavorite = async () => {
        await addFavorite(name);
        setName("");
        onClose();
        onAdded();
    }

    return (
        <Modal isOpen={isOpen} onClose={onClose} >
            <h2 className="modal-title">新增播放清單</h2>
            <input className="modal-input" type="text" value={name} onChange={(e) => setName(e.target.value)} />
            <input className="modal-btn" type="button" value={"新增"} onClick={() => handleAddFavorite()} disabled={name.length === 0} />
        </Modal>
    )
}

const AddFavoriteButton = ({favorites, onAdded}) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            {favorites.length < 10 && (
                <div className="favorite-item" onClick={() => setIsOpen(true)}>
                    <div className="favorite-add-btn">
                        <Icon.Plus />
                        <p>{favorites.length} / 10</p>
                    </div>
                </div>
            )}
            <AddFavoriteModal isOpen={isOpen} onClose={() => setIsOpen(false)} onAdded={onAdded} />
        </>
    )
}

const FavoritesGallery = () => {
    const [favorites, setFavorites] = useState([]);

    const fetchFavorites = useCallback(async () => {
        const data = await getFavorites();
        if (data) {
            setFavorites(data.result);
        }
    }, []);

    useEffect(() => {
        fetchFavorites();
    }, [fetchFavorites]);

    return (
        <div className="favorites-gallery">
            {favorites.map((item) => (
                <div className="favorite-item" key={item._id}>
                    <div className="favorite-cover" onClick={() => addToPlaylist(item._id, 'favorite')}>
                        <img src={item.thumbnails[0] || "/src/assets/black.png"} alt="" />
                        <img src={item.thumbnails[1] || "/src/assets/black.png"} alt="" />
                        <img src={item.thumbnails[2] || "/src/assets/black.png"} alt="" />
                        <img src={item.thumbnails[3] || "/src/assets/black.png"} alt="" />

                        <div className="favorite-cover-overlay">
                            <Icon.PlusCircle />
                        </div>
                    </div>
                    <a href={"/favorite/" + item._id} className="favorite-name">
                        {item.name}
                    </a>
                </div>
            ))}
            
            <AddFavoriteButton favorites={favorites} onAdded={fetchFavorites} />
        </div>
    )
}

const HomePage = () => {
    return (
        <div className="page home-page">
            <h1>Welcome to Pica</h1>
            <FavoritesGallery />
        </div>
    )
}

export default HomePage;