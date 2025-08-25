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

    const handleSearch = () => {
        if (keyword.trim() !== '') {
            navigate(`/search/${encodeURIComponent(keyword)}`);
        }
    }

    return (
        <div className="search-bar">
            <input type="search" autoComplete='search' value={keyword} onChange={handleInputChange} onKeyDown={(e) => {if (e.key === 'Enter') { handleSearch() }}} placeholder="Search..." />
            <Icon.Search className='search-icon' size={20} onClick={() => handleSearch()} />
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