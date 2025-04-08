import { useState, useEffect, createContext } from 'react'
import  { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import axiosInstance, {setInterceptor} from './utils/axiosInstance';
import './App.css'
import './styles/style.scss'

import Header from './pages/header';
import Footer from './pages/footer'
import FooterExpand from './pages/footerExpand';
import HomePage from './pages/homePage';
import SearchPage from './pages/searchPage';
import ErrorPage from './pages/errorPage';




const App = () => {
    const [expand, setExpand] = useState(false);
    const [userInfo, setUserInfo] = useState({});
    
    const navigate = useNavigate();
    setInterceptor(axiosInstance, navigate);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axiosInstance.get('/auth/get');
                setUserInfo(response.data);
                console.log(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchUser();
    }, [])

    return (
        <>
            <Header />

            <Routes>
                <Route path='/' element={<HomePage />}  />
                <Route path='/search/:keyword' element={<SearchPage />}  />
                <Route path='/error/:code' element={<ErrorPage />}  />
                <Route path='*' element={<Navigate to={'/'} />}  />
            </Routes>

            <Footer expand={expand} setExpand={setExpand} />
            <FooterExpand expand={expand} setExpand={setExpand} />
        </>
    )
}

export default App
