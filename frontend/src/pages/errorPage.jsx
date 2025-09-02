import React from "react";
import { useParams } from "react-router-dom";
import logo from '../assets/logo.svg'
import '../styles/page.scss'


const ErrorPage = () => {
    const {code} = useParams();
    const errorMessage = {
        401: '請重新至 Discord 使用 /web 登入',
        404: '請加入語音頻道再嘗試',
    }
    return (
        <div className="page error-page">
            <img src={logo} alt="" />
            <h1>{errorMessage[code]}</h1>
        </div>
    )
}

export default ErrorPage;