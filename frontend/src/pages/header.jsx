import React, { useState, useEffect, useContext } from 'react'
import { useNavigate } from 'react-router-dom';
import * as Icon from 'react-feather';
import '../styles/main.scss'
import logo from '../assets/pica.svg'
import axiosInstance from '../utils/axiosInstance';
import PlaybackContext from '../context/PlaybackContext';


const SearchBar = () => {
    const [keyword, setKeyword] = useState('');
    const navigate = useNavigate();

    const handleInputChange = (event) => {
        setKeyword(event.target.value);
    };

    return (
        <div className="search-bar">
            <input type="text" value={keyword} onChange={handleInputChange} placeholder="Search..." />
            <Icon.Search className='search-icon' size={20} onClick={() => navigate(`/search/${keyword}`)} />
        </div>
    );
}

const Header = () => {
    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axiosInstance.get('/auth/get');
                console.log(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchUser();
    }, [])
    return (
        <header className="header">
            <div className='logo'>
                <img src={logo} />
                <h1>Pica</h1>
            </div>
            <SearchBar />

        </header>
    )
}

export default Header