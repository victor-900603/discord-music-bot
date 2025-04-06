import React, { useState, useEffect, useContext } from 'react'
import { useParams } from 'react-router-dom';
import * as Icon from 'react-feather';
import '../styles/page.scss'
import axiosInstance from '../utils/axiosInstance';


const SearchItem = ({ song }) => {
    const { videoId, title, thumbnail, length, channel } = song;

    const handAddToPlaylist = async (id) => {
        try {
            const response = await axiosInstance.get('/playlist/add?id=' + id);
            console.log(response.data);
        } catch (error) {
            console.error('Error AddToPlaylist:', error);
        }
    }

    return (
        <li className='search-item'>
            <div className='search-item-content'>
                <img src={thumbnail} alt={song.title} />
                <div className='search-item-info'>
                    <h2>{title}</h2>
                    <p>{channel}</p>
                    <p>{length}</p>
                </div>
            </div>
            <div className='search-item-action' onClick={() => handAddToPlaylist(videoId)}>
                <Icon.PlusCircle />
            </div>
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