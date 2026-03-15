import React, { useContext, useCallback } from 'react'
import * as Icon from 'react-feather';
import '../styles/main.scss'

import { pause, play, skiptoIndex, toggleLoop, toggleShuffle, setVolume } from '../api/playback';
import PlaybackContext from '../context/PlaybackContext';
import PlayingSong from '../components/playingSong';

const Controller = () => {
    const { playing, loop, shuffle, volume, currentIndex, playlist } = useContext(PlaybackContext);

    const handlePlayPause = useCallback(async () => {
        if (playing) {
            await pause();
        } else {
            await play();
        }
    }, [playing]);

    const handleVolumeChange = useCallback(async (e) => {
        const val = parseFloat(e.target.value);
        await setVolume(val);
    }, []);

    return (
        <div className="controller">
            <button className='shuffle-btn' onClick={() => toggleShuffle()}>
                <Icon.Shuffle className={shuffle ? 'active' : ''} />
            </button>
            <button className='skip-btn' disabled={currentIndex <= 0} onClick={() => skiptoIndex(currentIndex - 1)}>
                <Icon.SkipBack />
            </button>
            <button className='play-btn' onClick={handlePlayPause}>
                {playing ? <Icon.Pause /> : <Icon.Play />}
            </button>
            <button className='skip-btn' disabled={currentIndex + 1 >= playlist.length} onClick={() => skiptoIndex(currentIndex + 1)}>
                <Icon.SkipForward />
            </button>
            <button className='loop-btn' onClick={() => toggleLoop()}>
                <Icon.Repeat className={loop ? 'active' : ''} />
            </button>
            <div className="volume-control">
                <Icon.Volume2 className="volume-icon" />
                <input
                    type="range"
                    className="volume-slider"
                    min="0"
                    max="1"
                    step="0.05"
                    value={volume}
                    onChange={handleVolumeChange}
                />
            </div>
        </div>
    )
}


const ExpandBtn = ({expand, setExpand}) => {
    return (
        <button className='expand-btn' onClick={() => setExpand(!expand)}>
            <Icon.ChevronUp className={expand ? 'expanded' : ''} />
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