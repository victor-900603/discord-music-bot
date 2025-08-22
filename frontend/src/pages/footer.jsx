import React, { useState, useContext } from 'react'
import * as Icon from 'react-feather';
import '../styles/main.scss'

import { pause, play, skiptoIndex, toggleLoop } from '../api/playback';
import PlaybackContext from '../context/PlaybackContext';
import PlayingSong from '../components/playingSong';

const Controller = () => {
    const { playing } = useContext(PlaybackContext);
    const { loop, setLoop, currentIndex, playlist } = useContext(PlaybackContext);


    const handlePlayPause = async () => {
        if (playing) {
            await pause();
        } else {
            await play();
        }
    }

    return (
        <div className="controller">
            <button className='skip-btn' disabled={(currentIndex <= 0)? true: false} onClick={() => skiptoIndex(currentIndex - 1)}>
                {<Icon.SkipBack />}
            </button>
            <button className='play-btn' onClick={handlePlayPause}>
                {playing ? <Icon.Pause /> : <Icon.Play />}
            </button>
            <button className='skip-btn' disabled={(currentIndex + 1 >= playlist.length)? true: false} onClick={() => skiptoIndex(currentIndex + 1)}>
                {<Icon.SkipForward />}
            </button>
            <button className='loop-btn' onClick={() => toggleLoop()}>
                {<Icon.Repeat className={loop? 'active': ''} />}
            </button>
        </div>
    )
}



const ExpandBtn = ({expand, setExpand}) => {
    return (
        <button className='expand-btn' onClick={() => setExpand(!expand)}>
            {<Icon.ChevronUp className={expand ? 'expanded': ''} />}
        </button>
    )

}

const Footer = ({expand, setExpand}) => {
    

    return (
        <footer className="footer">
            <PlayingSong />
            <Controller />
            <ExpandBtn expand={expand} setExpand={setExpand} />
        </footer>
    )
}

export default Footer