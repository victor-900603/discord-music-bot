import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';


const PlaybackContext = createContext();

export function PlaybackProvider({ children }) {
    const [playing, setPlaying] = useState(false);
    const [loop, setLoop] = useState(false);
    const [playlist, setPlaylist] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(-1);

    const defaultSong = {
        title: "",
        thumbnail: "/src/assets/disc.webp",
        channel: "",
    };
    const [currentSong, setCurrentSong] = useState(defaultSong);

    const navigate = useNavigate();

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/playback/");
        ws.onopen = () => console.log("WebSocket 連線成功");
    
        ws.onmessage = (event) => {
            const receivedData = JSON.parse(event.data);
            const { is_playing, loop, songs, current_index } = receivedData;

            setPlaying(is_playing);
            setLoop(loop);
            setPlaylist(songs);
            setCurrentIndex(current_index);
            setCurrentSong(songs[current_index]);
            if (songs[current_index]) {
                setCurrentSong(songs[current_index]);
            } else {
                setCurrentSong(defaultSong);
            }
            
        };
    
        ws.onerror = (error) => {
            console.error("WebSocket 錯誤:", error);
            navigate('/error/404');
        };
        ws.onclose = () => console.log("WebSocket 連線關閉");
    
        // return () => ws.close();
      }, []);
  
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