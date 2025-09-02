import { useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { auth } from "../api/auth";

const AuthPage = () => {
    const [searchParams] = useSearchParams();
    const token = searchParams.get("token");
    const navigate = useNavigate();

    useEffect(() => {
        if (token) {
            (async () => {
                const data = await auth(token);
                if (data) {
                    navigate('/');
                }
            })();
        }

    },[token]);

    return (
        <div className="page auth-page">

        </div>
    )
}

export default AuthPage;