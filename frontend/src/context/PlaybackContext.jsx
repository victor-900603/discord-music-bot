import React, { createContext, useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

const WS_URL = import.meta.env.VITE_WS_URL;
const RECONNECT_DELAY_MS = 3000;
const MAX_RECONNECT_ATTEMPTS = 10;
const DEFAULT_SONG = {
    title: "",
    thumbnail: "/src/assets/disc.webp",
    channel: "",
};

const PlaybackContext = createContext();

export function PlaybackProvider({ children }) {
    const [playing, setPlaying] = useState(false);
    const [loop, setLoop] = useState(false);
    const [shuffle, setShuffle] = useState(false);
    const [volume, setVolume] = useState(0.5);
    const [playlist, setPlaylist] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(-1);
    const [connected, setConnected] = useState(false);

    const [currentSong, setCurrentSong] = useState(DEFAULT_SONG);

    const navigate = useNavigate();
    const wsRef = useRef(null);
    const reconnectAttempts = useRef(0);
    const reconnectTimer = useRef(null);

    const connectWebSocket = useCallback(() => {
        if (wsRef.current?.readyState === WebSocket.OPEN) return;

        const ws = new WebSocket(WS_URL);
        wsRef.current = ws;

        ws.onopen = () => {
            console.log("WebSocket 連線成功");
            setConnected(true);
            reconnectAttempts.current = 0;
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const { is_playing, loop: loopState, shuffle: shuffleState, volume: vol, songs, current_index } = data;

            setPlaying(is_playing);
            setLoop(loopState);
            setShuffle(shuffleState ?? false);
            setVolume(vol ?? 0.5);
            setPlaylist(songs);
            setCurrentIndex(current_index);
            setCurrentSong(songs[current_index] ?? DEFAULT_SONG);
        };

        ws.onerror = (error) => {
            console.error("WebSocket 錯誤:", error);
        };

        ws.onclose = (event) => {
            console.log("WebSocket 連線關閉", event.code);
            setConnected(false);
            wsRef.current = null;

            // 自動重連
            if (reconnectAttempts.current < MAX_RECONNECT_ATTEMPTS) {
                reconnectAttempts.current += 1;
                const delay = RECONNECT_DELAY_MS * Math.min(reconnectAttempts.current, 5);
                console.log(`將在 ${delay}ms 後嘗試第 ${reconnectAttempts.current} 次重連...`);
                reconnectTimer.current = setTimeout(connectWebSocket, delay);
            } else {
                console.error("WebSocket 重連次數已達上限");
                navigate('/error/404');
            }
        };
    }, [navigate]);

    useEffect(() => {
        if (!window.location.pathname.startsWith('/auth')) {
            connectWebSocket();
        }
        return () => {
            clearTimeout(reconnectTimer.current);
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [connectWebSocket]);

    return (
        <PlaybackContext.Provider 
            value={{ 
                playing, setPlaying,
                currentSong, setCurrentSong,
                currentIndex, setCurrentIndex,
                playlist, setPlaylist,
                loop, setLoop,
                shuffle, setShuffle,
                volume, setVolume,
                connected,
             }}>
            {children}
        </PlaybackContext.Provider>
    );
}

export default PlaybackContext;