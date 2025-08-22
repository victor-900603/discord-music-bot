
import * as Icon from 'react-feather';

const Modal = ({children, isOpen, onClose}) => {
    if (!isOpen) return null;
    return (
        <div className="modal-overlay">
            <div className='modal'>
                <Icon.X className='close-btn' onClick={onClose} />
                {children}

            </div>
        </div>
    )
}


export default Modal;