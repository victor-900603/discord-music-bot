import React, { useEffect, useContext, useRef } from 'react'
import * as Icon from 'react-feather';

import PlaybackContext from '../context/PlaybackContext';


const PlayingSong = () => {
    const { playing, currentSong } = useContext(PlaybackContext);
    const rotatingImage = useRef(null);
    const rotationInterval = useRef(null);
    const currentRotation = useRef(0);
      
    function rotateImage() {
        currentRotation.current += 1;
        rotatingImage.current.style.transform = `rotate(${currentRotation.current}deg)`;
    }

    useEffect(() => {
        if (playing) {
            rotationInterval.current = setInterval(rotateImage, 50);
        } else {
            clearInterval(rotationInterval.current);
        }
    }, [playing]);

    return (
        <div className='playing-song'>
            <div className="song-cover">
                <img src={currentSong.thumbnail} ref={rotatingImage} id="rotatingImage" alt="" />
                <span className="point"></span>
            </div>
            <div className='song-info'>
                <h2>{currentSong.title}</h2>
                <p>{currentSong.channel}</p>
            </div>
        </div>

    )
}

export default PlayingSong;