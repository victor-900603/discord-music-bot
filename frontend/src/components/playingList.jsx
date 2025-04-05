import React, { useEffect, useContext, useRef } from 'react'
import * as Icon from 'react-feather';

import axiosInstance from '../utils/axiosInstance';
import PlaybackContext from '../context/PlaybackContext';


const Song = ({index, song, current}) => {

    const handleSkipto = async (index) => {
        try {
            const response = await axiosInstance.get(`/playback/skipto?index=${index}`);
            console.log(response.data);
        } catch (error) {
            console.error('Error skipping to song:', error);
        }
    }

    return (
        <li className={current? 'song current' : 'song'} onClick={handleSkipto.bind(null, index)}>
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
                <Song key={index} index={index} song={song} current={index==currentIndex} />
            ))}
        </ul>

    )
}

export default PlayingList;