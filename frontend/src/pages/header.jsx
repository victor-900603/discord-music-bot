import React, { useState, useEffect, useContext } from 'react'
import { useNavigate, Link } from 'react-router-dom';
import * as Icon from 'react-feather';
import '../styles/main.scss'
import logo from '../assets/logo.svg'


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

    return (
        <header className="header">
            <Link to={'/'}>
                <div className='logo'>
                    <img src={logo} />
                    <h1>Pica</h1>
                </div>
            </Link>
            <SearchBar />

        </header>
    )
}

export default Header