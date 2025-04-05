import React, { useState, useContext } from 'react'
import * as Icon from 'react-feather';
import '../styles/footer.scss'

import PlaybackContext from '../context/PlaybackContext';
import PlayingSong from '../components/playingSong';

const Controller = () => {
    const { playing, setPlaying } = useContext(PlaybackContext);
    const { loop, setLoop, currentIndex, setCurrentIndex } = useContext(PlaybackContext);
    return (
        <div className="controller">
            <button className='skip-btn' onClick={() => setCurrentIndex(currentIndex - 1)}>
                {<Icon.SkipBack />}
            </button>
            <button className='play-btn' onClick={() => setPlaying(!playing)}>
                {playing ? <Icon.Pause /> : <Icon.Play />}
            </button>
            <button className='skip-btn' onClick={() => setCurrentIndex(currentIndex + 1)}>
                {<Icon.SkipForward />}
            </button>
            <button className='loop-btn' onClick={() => setLoop(!loop)}>
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