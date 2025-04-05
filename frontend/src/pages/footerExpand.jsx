import React, { useState, useContext } from 'react'
import * as Icon from 'react-feather';

import PlaybackContext from '../context/PlaybackContext';
import PlayingSong from '../components/playingSong';
import PlayingList from '../components/playingList';

const FooterExpand = ({expand, setExpand}) => {

    return (
        <div className={expand ? 'footer-expand expanded' : 'footer-expand'}>
            <PlayingSong />
            <PlayingList />
        </div>
    )
}

export default FooterExpand;