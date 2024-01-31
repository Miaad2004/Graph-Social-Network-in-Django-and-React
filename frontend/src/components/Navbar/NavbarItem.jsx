import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import styles from './NavbarItem.module.css';
import { Link } from 'react-router-dom';

function NavbarItem(props) {
    return (
        <li className="nav-item mb-2">
            <Link to={props.to} className={`nav-link text-white ${styles.navlink}`} onClick={props.onClick}>
                <FontAwesomeIcon icon={props.icon} size={props.size} className='fa-fw me-2'/>
                {props.text}
            </Link>
        </li>
    );
}

NavbarItem.propTypes = {
    icon: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired,
    size: PropTypes.string,
    to: PropTypes.string,
    onClick: PropTypes.func,
};

NavbarItem.defaultProps = {
    size: "lg",
};

export default NavbarItem;