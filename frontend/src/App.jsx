import { useState, createContext } from 'react'
import  { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import './styles/style.scss'

import { PlaybackProvider } from './context/PlaybackContext';
import Header from './pages/header';
import Footer from './pages/footer'
import FooterExpand from './pages/footerExpand';
import SearchPage from './pages/searchPage';




const App = () => {
    const [expand, setExpand] = useState(false);

    return (
        <PlaybackProvider>
            <Router>
                <Header />

                <Routes>
                    <Route path='/search/:keyword' element={<SearchPage />}  />
                    <Route path='/test' element={<Link to="/search">PAGE2</Link>}  />
                </Routes>

                <Footer expand={expand} setExpand={setExpand} />
                <FooterExpand expand={expand} setExpand={setExpand} />
            </Router>
        </PlaybackProvider>
    )
}

export default App
