import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

import  { BrowserRouter as Router } from 'react-router-dom';
import { PlaybackProvider } from './context/PlaybackContext';
import { ToastContextProvider } from './context/ToastContext.jsx';



createRoot(document.getElementById('root')).render(
    <StrictMode>
        <Router>
            <ToastContextProvider>
                <PlaybackProvider>
                    <App />
                </PlaybackProvider>
            </ToastContextProvider>
        </Router>
    </StrictMode>
)
