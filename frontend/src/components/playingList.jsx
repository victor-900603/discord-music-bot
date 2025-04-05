import React, { useEffect, useContext, useRef } from 'react'
import * as Icon from 'react-feather';

import PlaybackContext from '../context/PlaybackContext';


const Song = ({song, current}) =>{
    return (
        <li className={current? 'song current' : 'song'}>
            <div className="cover">
                <img src={song.thumbnail} alt="" />
            </div>
            <div className='info'>
                <h2 title={song.title}>{song.title}</h2>
                <p>{song.channel}</p>
            </div>
        </li>
    )
}

const PlayingList = () => {
    const { playlist, currentIndex } = useContext(PlaybackContext);



    return (
        <ul className='playing-list'>
            {playlist.map((song, index) => (
                <Song key={index} song={song} current={index==currentIndex} />
            ))}
        </ul>

    )
}

export default PlayingList;