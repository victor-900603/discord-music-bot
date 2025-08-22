import React, { useEffect, useContext, useRef, useState } from 'react'
import * as Icon from 'react-feather';

import axiosInstance from '../utils/axiosInstance';
import PlaybackContext from '../context/PlaybackContext';


const Song = ({index, song, current}) => {
    const [open, setOpen] = useState(false)
    const menuRef = useRef(null)

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (menuRef.current && !menuRef.current.contains(e.target)) {
                setOpen(false);
            }
        }

        document.addEventListener('click', handleClickOutside)
        return () => {
            document.removeEventListener('click', handleClickOutside)
        }
    }, [])

    const handleSkipto = async (index) => {
        try {
            setOpen(false);
            const response = await axiosInstance.get(`/playback/skipto?index=${index}`);
            console.log(response.data);
        } catch (error) {
            console.error('Error skipping to song:', error);
        }
    }

    const handleRemove = async (index) => {
        try {
            const response = await axiosInstance.delete(`/playlist?index=${index}`);
            console.log(response.data);
        } catch (error) {
            console.error('Error removing song:', error);
        }
    }



    return (
        <li className={current? 'song current' : 'song'} ref={menuRef}>
            <div className='song-btn' onClick={handleSkipto.bind(null, index)}>
                <div className="cover">
                    <img src={song.thumbnail} alt="" />
                </div>
                <div className='info'>
                    <h2 title={song.title}>{song.title}</h2>
                    <p>{song.channel}</p>
                </div>
            </div>

            <div className='more-btn' onClick={() => setOpen(!open)}>
                <Icon.MoreVertical className='more-icon' />
            </div>
            
            {open && (
                <div className="menu">
                    <a className='option' href={song.webpage_url} target='_blank'>
                        <Icon.Globe /> 
                        <span>前往</span>
                    </a>
                    <div className="option">
                        <Icon.Heart /> 
                        <span>收藏</span>
                    </div>
                    <div className="option delete-btn" onClick={handleRemove.bind(null, index)}>
                        <Icon.Trash /> 
                        <span>刪除</span>
                    </div>
                </div>
            )} 
        </li>
    )
}

const PlayingList = () => {
    const { playlist, currentIndex } = useContext(PlaybackContext);



    return (
        <ul className='playing-list'>
            {playlist.map((song, index) => (
                <Song key={index} index={index} song={song} current={index==currentIndex} />
            ))}
        </ul>

    )
}

export default PlayingList;