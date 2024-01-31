import React from 'react';
import PropTypes from 'prop-types';
import { Container, Nav, Image } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavbarItem from './NavbarItem';
import defaultUserImage from '../../assets/profile_image_placeholder.jpg';
import { AxiosContext, LoginContext, API_URL } from '../../App';
import { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie'; 

function Navbar(props) {
    const { loginState, setLoginState } = useContext(LoginContext);
    const client = useContext(AxiosContext);
    const navigate = useNavigate();

    const [user, setUser] = useState({
        imagePath: defaultUserImage,
        userName: 'User Name',
        university: 'University',
    });

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await client.post('/api/get_user/');
                console.log(response);

                setUser({
                    imagePath: response.data.user.profile_photo ? API_URL + response.data.user.profile_photo: defaultUserImage,
                    userName: response.data.user.username || 'User Name',
                    university: response.data.user.university || 'University',
                    field: response.data.user.field || 'Field',
                });
            } 
            
            catch (error) {
                console.error("Error fetching user data: ", error);
            }
        };

        fetchUserData();
    }, [client]);

    const handleDeleteAccount = async (e) => {
        if(window.confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
            try {
                await client.delete('/api/delete_account/');
                delete client.defaults.headers.common["Authorization"];
                setLoginState({ isLoggedIn: false, userName: null });
                navigate('/login');
            }
            
            catch (error) {
                console.error("Error deleting account: ", error);
            }
        }
    };

    const handleLogout = async (e) => {
        try {
            await client.post('/api/logout/');
            delete client.defaults.headers.common["Authorization"];
            setLoginState({ isLoggedIn: false, userName: null });
            navigate('/login');
        }
        
        catch (error) {
            console.error("Logout failed: ", error);
        }
    };

    return (
        <Container fluid className="p-0 d-flex h-100">
            <div id="bdSidebar"
                className="d-flex flex-column
                            p-3 bg-dark
                            text-white">

                <div className="d-flex flex-column justify-content-center align-items-center">
                    <Image src={user.imagePath} roundedCircle width={128} height={128} />
                    <p className="text-center mt-2">{user.userName}<br />{user.university}<br />{user.field}</p>
                </div>
                <hr className="my-2" />
                <Nav className="flex-column">
                    <NavbarItem to='/connections' text="Connections" icon="fa-solid fa-diagram-project" />
                    <NavbarItem to='/suggestions' text="Suggestions" icon="fa-solid fa-wand-magic-sparkles"/>
                    <NavbarItem to='/search' text="View All Users" icon="fa-solid fa-users"/>
                    <NavbarItem text="Delete Account" icon="fa-solid fa-trash" onClick={handleDeleteAccount}/>
                    <NavbarItem text="Logout" icon="fa-solid fa-right-from-bracket" onClick={handleLogout}/>
                </Nav>
            </div>
        </Container>
    );
}

Navbar.propTypes = {
    imagePath: PropTypes.string,
    userName: PropTypes.string,
};

Navbar.defaultProps = {
    imagePath: defaultUserImage, 
    userName: 'User Name',
};

export default Navbar;