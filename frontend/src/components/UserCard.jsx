import React from 'react';
import PropTypes from 'prop-types';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import defaultUserImage from '../assets/profile_image_placeholder.jpg';

const UserCard = ({ user, onConnect, onRemoveConnection }) => {
    return (
        <Card style={{ width: '18rem', height:'500px', padding: '10px', margin: '10px' }}>
            <Card.Img variant="top" src={user.profile_photo || defaultUserImage} className='mx-auto d-block rounded-circle' style={{ width: '100px', height: '100px' }} />
            <Card.Body className="d-flex flex-column align-items-center text-center" style={{ overflowY: 'auto' }}>
                <Card.Title>{user.username}</Card.Title>
                <Card.Text>{user.university}</Card.Text>
                <Card.Text>Birthday: {user.birthday}</Card.Text>
                <Card.Text>Field: {user.field}</Card.Text>
                <Card.Text>Workplace: {user.workplace}</Card.Text>
                <Card.Text>Specialities: {user.specialties}</Card.Text>
            </Card.Body>

            {user.isConnected ? (
                    <Button variant="danger" onClick={() => onRemoveConnection(user.username, 'disconnect')}>Remove Connection</Button>
                ) : (
                    <Button variant="primary" onClick={() => onConnect(user.username, 'connect')}>Connect</Button>
                )}
        </Card>
    );
};

UserCard.propTypes = {
    user: PropTypes.shape({
        profile_photo: PropTypes.string,
        username: PropTypes.string,
        birthday: PropTypes.string,
        university: PropTypes.string,
        field: PropTypes.string,
        workplace: PropTypes.string,
        specialties: PropTypes.string,
    }),
    isConnected: PropTypes.bool,
    onConnect: PropTypes.func,
    onRemoveConnection: PropTypes.func,
};

UserCard.defaultProps = {
    user: {
        profile_photo: defaultUserImage,
        username: 'Anonymous',
        birthday: 'Unknown',
        university: 'Uni',
        field: 'Unknown',
        workplace: 'Unknown',
        specialties: '',
    },
    isConnected: false,
    onConnect: () => {},
    onRemoveConnection: () => {},
};

export default UserCard;