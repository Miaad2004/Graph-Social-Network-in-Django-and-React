import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import 'bootstrap/dist/css/bootstrap.min.css';

function FileInput(props) {
    return <input type="file" className="form-control-file mt-1" {...props} />;
}

function TextInput(props) {
    return <input className="form-control mt-1" {...props}/>;
}

function FormInputField(props) {
    const {icon, label, type, id} = props;
    return (
        <div className="form-group mb-5">
            <FontAwesomeIcon icon={icon} className="me-2"/>
            <label htmlFor={id}>{label}</label>
            {type === "file" ? 
                <FileInput {...props} /> :
                <TextInput {...props}/>
            }
        </div>
    )
}

export default FormInputField;