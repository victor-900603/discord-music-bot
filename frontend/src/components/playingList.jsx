import React, { useEffect, useContext, useRef, useState } from 'react'
import * as Icon from 'react-feather';

import PlaybackContext from '../context/PlaybackContext';
import { skiptoIndex } from '../api/playback';
import { removeFromPlaylist } from '../api/playlist';

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
        setOpen(false);
        await skiptoIndex(index);
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
                    <div className="option delete-btn" onClick={() => removeFromPlaylist(index)}>
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