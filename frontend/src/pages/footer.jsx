import React, { useState, useContext } from 'react'
import * as Icon from 'react-feather';
import '../styles/footer.scss'
import axiosInstance from '../utils/axiosInstance';

import PlaybackContext from '../context/PlaybackContext';
import PlayingSong from '../components/playingSong';

const Controller = () => {
    const { playing } = useContext(PlaybackContext);
    const { loop, setLoop, currentIndex, playlist } = useContext(PlaybackContext);


    const handlePlayPause = async () => {
        try {
            if (playing) {
                const response = await axiosInstance.get('/playback/pause');
                console.log(response.data);
            } else {
                const response = await axiosInstance.get('/playback/play');
                console.log(response.data);
            }
            
            
        } catch (error) {
            console.error('Error toggling play/pause:', error);
        }
    }

    const handleSkipto = async (index) => {
        try {
            const response = await axiosInstance.get(`/playback/skipto?index=${index}`);
            console.log(response.data);
        } catch (error) {
            console.error('Error skipping to song:', error);
        }
    }

    const handleLoop = async () => {
        try {
            const response = await axiosInstance.get('/playback/loop');
            console.log(response.data);
        } catch (error) {
            console.error('Error toggling loop:', error);
        }
    }

    return (
        <div className="controller">
            <button className='skip-btn' disabled={(currentIndex <= 0)? true: false} onClick={handleSkipto.bind(null, currentIndex - 1)}>
                {<Icon.SkipBack />}
            </button>
            <button className='play-btn' onClick={handlePlayPause}>
                {playing ? <Icon.Pause /> : <Icon.Play />}
            </button>
            <button className='skip-btn' disabled={(currentIndex + 1 >= playlist.length)? true: false} onClick={handleSkipto.bind(null, currentIndex + 1)}>
                {<Icon.SkipForward />}
            </button>
            <button className='loop-btn' onClick={handleLoop}>
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