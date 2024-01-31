import React, { useState, useContext } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './SignUpForm.module.css'; 
import FormInputField from './FormInputField';
import { Link, useNavigate } from 'react-router-dom';
import Notification from '../Notification.jsx';
import { AxiosContext } from '../../App';

const initialFormState = {
    username: '',
    password: '',
    birthday: '',
    university: '',
    field: '',
    workplace: '',
    specialties: '',
    profile_photo: null,
};

function SignUpForm() {
    const [formState, setFormState] = useState(initialFormState);
    const [toast, setToast] = useState({show: false, message: '', type: ''});
    const [loading, setLoading] = useState(false); 
    
    const client = useContext(AxiosContext);
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        setFormState({
            ...formState,
            [e.target.id]: e.target.value,
        });
    };

    const handleFileChange = (e) => {
        console.log(e.target.files)
        setFormState({
            ...formState,
            profile_photo: e.target.files[0],
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true); 

        try {
            const response = await client.post('/api/register/', formState, {
                headers: {
                  'content-type': 'multipart/form-data'
                }
              });
            console.log(response);
            
            if (response.data.error && response.data.error.trim() !== "")
                throw new Error(response.data.error);

            if (response.data) {
                setToast({show: true, message: 'Sign up successful!', type: 'success'});
                setTimeout(() => {
                    navigate('/login');
                }, 500);
            }

        } 
        
        catch (error) {
            console.error("Sign Up failed: ", error);
            const serverErrorMessage = Object.entries(error.response?.data || {}).map(([key, value]) => `${key}: ${value}`).join('\n');
            setToast({show: true, message: serverErrorMessage, type: 'error'});
            
        } 
        
        finally {
            setLoading(false); 
        }
    };

    return (
    <div className={`container-fluid ${styles.formBody} d-flex justify-content-center align-items-center`}>
        <div className={styles.signUpForm}> 
            <form onSubmit={handleSubmit}>
                <h1> Sign Up </h1>
                <div className="row pt-2">
                    <div className="col-md-6">
                        <FormInputField id="username" icon="fa-solid fa-user" label="Username" type="text" placeholder="Enter your username" value={formState.username} onChange={handleInputChange} />
                        <FormInputField id="password" icon="fa-solid fa-lock" label="Password" type="password" placeholder="Enter your password" value={formState.password} onChange={handleInputChange} />
                        <FormInputField id="birthday" icon="fa-solid fa-calendar" label="Birthday" type="date" value={formState.birthday} onChange={handleInputChange} />
                        <FormInputField id="university" icon="fa-solid fa-university" label="University" type="text" placeholder="Enter your university" value={formState.university} onChange={handleInputChange} />
                    </div>
                    <div className="col-md-6">
                        <FormInputField id="field" icon="fa-solid fa-map-marker-alt" label="field" type="text" placeholder="Enter your field" value={formState.field} onChange={handleInputChange} />
                        <FormInputField id="workplace" icon="fa-solid fa-briefcase" label="Workplace" type="text" placeholder="Enter your workplace" value={formState.workplace} onChange={handleInputChange} />
                        <FormInputField id="specialties" icon="fa-solid fa-tags" label="Specialties" type="text" placeholder="Enter your specialties, separated by commas" value={formState.specialties} onChange={handleInputChange} />
                        <FormInputField id="profile_photo" icon="fa-solid fa-image" label="Profile Image" type="file" accept="image/*" onChange={handleFileChange} />
                    </div>
                </div>

                <button type="submit" className="btn btn-primary btn-lg btn-block w-100" disabled={loading}>
                    {loading ? <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> : 'Sign Up'}
                </button>

                <div className={`form-group text-center mt-3 ${styles.signUpLink}`}> 
                    <p>Already have an account? <Link to="/login" className='text-decoration-none'>Login here</Link></p>
                </div>
            </form>
        </div>

        {toast.show && <Notification title="Sign up Status" message={toast.message} 
        type={toast.type} show={toast.show} onClose={() => setToast({ ...toast, show: false })} />}
    </div>
    )
}

export default SignUpForm;