import React from 'react';
import { Toast } from 'react-bootstrap';

function Notification({ title, message, type, show, onClose }) {
    const headerClass = type === 'success' ? 'text-success' : type === 'error' ? 'text-danger' : 'text-warning';
    const toastStyle = type === 'success' ? { borderColor: 'green' } : type === 'error' ? { borderColor: 'red' } : { borderColor: 'orange' };

    return (
        <div className="d-flex justify-content-end position-absolute top-0 end-0 p-3" style={{zIndex: 9999}}>
            <Toast onClose={onClose} show={show} delay={6000} autohide style={toastStyle}>
                <Toast.Header>
                    <strong className={`me-auto m-1 ${headerClass}`}>{title}</strong>
                </Toast.Header>
                <Toast.Body>
                    {message.split('\n').map((item, key) => {
                        return <p key={key}>{item}</p>
                    })}
                </Toast.Body>
            </Toast>
        </div>
    );
}

export default Notification;