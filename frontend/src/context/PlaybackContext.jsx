import React, { createContext, useState } from 'react';



const PlaybackContext = createContext();

export function PlaybackProvider({ children }) {
    const [playing, setPlaying] = useState(false);
    const [loop, setLoop] = useState(false);
    const [playlist, setPlaylist] = useState([
        {
            title: '任性 (電視劇《難哄》主題曲)',
            channel: '五月天 (Mayday)',
            thumbnail: 'https://i.ytimg.com/vi/d9ktAt-Gg2k/hq720.jpg'
        },
        {
            title: 'MAYDAY 五月天 [ 擁抱 Embrace ] Official Live Video',
            channel: '相信音樂BinMusic',
            thumbnail: 'https://i.ytimg.com/vi/rS8HqJy1UPs/hq720.jpg'
        },
        {
            title: 'MAYDAY五月天 [ 為你寫下這首情歌 Song for You ] Official Music Video',
            channel: '五月天 (Mayday)',
            thumbnail: 'https://i.ytimg.com/vi/V9sWPHGbESM/hq720.jpg'
        }
    ]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [currentSong, setCurrentSong] = useState({
        title: '任性 (電視劇《難哄》主題曲)',
        channel: '五月天 (Mayday)',
        thumbnail: 'https://i.ytimg.com/vi/d9ktAt-Gg2k/hq720.jpg'
    })
  
    return (
        <PlaybackContext.Provider 
            value={{ 
                playing, setPlaying,
                currentSong, setCurrentSong,
                currentIndex, setCurrentIndex,
                playlist, setPlaylist,
                loop, setLoop,
             }}>
            {children}
        </PlaybackContext.Provider>
    );
}

export default PlaybackContext;