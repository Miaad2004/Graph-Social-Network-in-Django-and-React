import { AxiosContext, LoginContext } from '../../App';
import 'bootstrap/dist/css/bootstrap.min.css';
import Cookies from 'js-cookie'; 
import { Link, useNavigate } from 'react-router-dom';
import Notification from '../Notification.jsx';
import React, { useContext, useState } from 'react';
import styles from './LoginForm.module.css'; 
import FormInputField from './FormInputField';


function LoginForm() {
    const initialFormState = {
        username: '',
        password: '',
    };

    const [formState, setFormState] = useState(initialFormState);
    const [toast, setToast] = useState({show: false, message: '', type: ''});
    const [loading, setLoading] = useState(false); 

    const { loginState, setLoginState } = useContext(LoginContext);
    const client = useContext(AxiosContext);
    const navigate = useNavigate();
    
    const handleInputChange = (e) => {
        setFormState({
            ...formState,
            [e.target.id]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true); 

        try {
            const response = await client.post('/api/login/', {username: formState.username, password: formState.password});
            
            if (response.data.error && response.data.error.trim() !== "") {
                throw new Error(response.data.error);
            }

            if (response.data && response.data.token) {
                setToast({show: true, message: 'Login successful!', type: 'success'});
                const token = response.data.token;
                client.defaults.headers.common['Authorization'] = `Token ${token}`;

                setLoginState({ isLoggedIn: true, userName: response.data?.user?.username });

                setTimeout(() => {
                    navigate('/connections');
                }, 500);
            }
            
        } 
        
        catch (error) {
            console.error("Login failed: ", error);
            setToast({show: true, message:  error.toString(), type: 'error'});
        } 
        
        finally {
            setLoading(false); 
        }
    };

    return (
    <div className={`container-fluid ${styles.formBody} d-flex justify-content-center align-items-center `}>
        <div className={styles.loginForm}> 
            <form onSubmit={handleSubmit}>
             
                <h1> Connection Recommender </h1>

                <FormInputField id="username" icon="fa-solid fa-user" label="Username" 
                type="text" placeholder="Enter your username" value={formState.username} onChange={handleInputChange} />

                <FormInputField id="password" icon="fa-solid fa-lock" label="Password" 
                type="password" placeholder="Enter your password" value={formState.password} onChange={handleInputChange} />

                <button type="submit" className="btn btn-primary btn-lg btn-block w-100" disabled={loading}>
                    {loading ? <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> : 'Login'}
                </button>

                <div className={`form-group text-center mt-3 ${styles.signUpLink}`}> 
                    <p>Don't have an account? <Link to="/signup" className='text-decoration-none'>Sign up here</Link></p>
                </div>

            </form>
        </div>

        {toast.show && <Notification title="Sign up Status" message={toast.message} 
        type={toast.type} show={toast.show} onClose={() => setToast({ ...toast, show: false })} />}
    </div>
    )
}

export default LoginForm;