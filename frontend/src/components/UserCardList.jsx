import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import UserCard from './UserCard'; 
import React, { useState, useContext, useEffect } from 'react';
import { AxiosContext } from '../App';
import Notification from './Notification.jsx';

function UserCardList({ users, setUsers, removeUserOnDisconnect = false})
{
    const client = useContext(AxiosContext);
    const [toast, setToast] = useState({show: false, message: '', type: ''});

    const handleOnConnect = async (username, mode) => {
        try
        {
            var url = mode == 'connect' ? '/api/add_connection/' : '/api/remove_connection/';
            const response = await client.post(url, {username: username});

            if (response.data.error && response.data.error.trim() !== "")
                throw new Error(response.data.error);

            if (response.data) {
                const msg = mode == 'connect' ? 'Connection added!' : 'Connection removed!';
                setToast({show: true, message: msg, type: 'success'});

                setUsers(users.map(user => {
                    if (user.username === username) {
                        return {
                            ...user,
                            isConnected: mode == 'connect' ? true : false,
                        };
                    }

                    return user;
                }));

                 if (mode == 'disconnect' && removeUserOnDisconnect) {
                     setUsers(users.filter(user => user.username !== username));
                }
            }
        }

        catch (error)
        {
            console.error("Error connecting to user: ", error);
            const serverErrorMessage = Object.entries(error.response?.data || {}).map(([key, value]) => `${key}: ${value}`).join('\n');
            setToast({show: true, message: serverErrorMessage, type: 'error'});
        }
    };

    return (
        <Container fluid>
            <Row xs="auto">
                {users.map((user, index) => (
                    <Col key={index}>
                        <UserCard user={user} onConnect={handleOnConnect} onRemoveConnection={handleOnConnect} />
                    </Col>
                ))}
            </Row>
            {toast.show && <Notification title="Sign up Status" message={toast.message} 
            type={toast.type} show={toast.show} onClose={() => setToast({ ...toast, show: false })} />}
        </Container>
    );
};

export default UserCardList;