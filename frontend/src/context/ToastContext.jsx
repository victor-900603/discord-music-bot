import { useContext, createContext, useState, useEffect } from "react";
import { setToastFunction } from "../utils/toastHelpler";

const ToastContext = createContext();

export function ToastContextProvider({children}) {
    const [toasts, setToasts] = useState([]);
    const addToast = (message, type='info', duration=3000) => {
        const id = Date.now() +Math.random();
        setToasts((prev) => [...prev, {id, message, type}]);
        setTimeout(() => {
            setToasts((prev) => prev.filter((t) => t.id !== id));
        }, duration)
    }

    useEffect(() => {
        setToastFunction(addToast);
    },[]);

    return (
        <ToastContext.Provider value={addToast}>
            {children}
            <div className="toast-container">
                {toasts.map((t) => (
                    <div key={t.id} className={`toast ${t.type}`}>
                        {t.message}
                    </div>
                ))}
            </div>
        </ToastContext.Provider>
    )
}

export const useToast =() => useContext(ToastContext);