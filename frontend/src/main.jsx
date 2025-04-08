import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

import  { BrowserRouter as Router } from 'react-router-dom';
import { PlaybackProvider } from './context/PlaybackContext';



createRoot(document.getElementById('root')).render(
    <StrictMode>
        <Router>
            <PlaybackProvider>
                <App />
            </PlaybackProvider>
        </Router>
    </StrictMode>,
)
