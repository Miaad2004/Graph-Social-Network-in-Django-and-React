import React from 'react';
import MyNavbar from '../Navbar/Navbar.jsx'
import UserCardList from '../UserCardList.jsx'
import { useState, useEffect, useContext } from 'react'
import { AxiosContext, LoginContext, API_URL } from '../../App.jsx';
import { Container, Row, Col, Form } from 'react-bootstrap';

function SearchView()
{
    const [users, setUsers] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const client = useContext(AxiosContext);

    useEffect(() => {
        const fetchUserData = async (query) => {
            try {
                const response = await client.get('/api/search/', { params: { query: query } });
                console.log(response);
                setUsers(response.data);
            } 
            
            catch (error) {
                console.error("Error fetching user data: ", error);
            }
        };

        fetchUserData(searchQuery);
    }, [client, searchQuery]);
    
    return(
        <Container fluid>
            <Row>
                <Col xs={2} className="vh-100 h-100 p-0 d-flex h-100">
                    <MyNavbar />
                </Col>
                <Col xs={10} className="vh-100 overflow-auto py-2"> 
                    <Row className="justify-content-md-center">
                        <Col md="auto">
                            <Form.Group>
                            <Form.Control
                                type="text"
                                placeholder="Search users"
                                value={searchQuery}
                                onChange={e => setSearchQuery(e.target.value)}
                                style={{ width: '400px' }} 
                            />
                            </Form.Group>
                        </Col>
                    </Row>

                    <UserCardList users={users} setUsers={setUsers} />
                </Col>
            </Row>
        </Container>
    )
}

export default SearchView