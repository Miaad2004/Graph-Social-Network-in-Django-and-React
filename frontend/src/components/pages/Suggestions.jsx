import React from 'react';
import MyNavbar from '../Navbar/Navbar.jsx'
import UserCardList from '../UserCardList.jsx'
import { useState, useEffect, useContext } from 'react'
import { AxiosContext, LoginContext, API_URL } from '../../App.jsx';
import { Container, Row, Col, Form } from 'react-bootstrap';

function Suggestions()
{
    const [users, setUsers] = useState([]);
    const client = useContext(AxiosContext);

    useEffect(() => {
        const fetchUserData = async (query) => {
            try {
                const response = await client.get('/api/get_suggestions/');
                console.log(response);
                setUsers(response.data);
            } 
            
            catch (error) {
                console.error("Error fetching user data: ", error);
            }
        };

        fetchUserData();
    }, [client]);
    
    return(
        <Container fluid>
        <Row>
            <Col xs={2} className="vh-100 h-100 p-0 d-flex h-100">
                <MyNavbar />
            </Col>
            <Col className="vh-100 overflow-auto">
            <UserCardList users={users} setUsers={setUsers} removeUserOnDisconnect={true} />
            </Col>
        </Row>
    </Container>
    )
}

export default Suggestions