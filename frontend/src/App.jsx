import { useState, useEffect } from 'react'
import './App.css'
import MyNavbar from './components/Navbar/Navbar.jsx'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faDiagramProject, faRightFromBracket, faUserPen, faTrash , faWandMagicSparkles, faLock, faUser, faCalendar, faUniversity, faMapMarkerAlt, faBriefcase, faTags, faImage, faUsers } from '@fortawesome/free-solid-svg-icons'
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Connections from "./components/pages/Connections.jsx"
import LoginForm from "./components/pages/LoginForm.jsx"
import SignUpForm from "./components/pages/SignUpForm.jsx"
import Suggestions from "./components/pages/Suggestions.jsx"
import SearchView from "./components/pages/SearchView.jsx"
import axios from 'axios'
import React, { createContext } from 'react';
import Cookies from 'js-cookie'; 
import UserCard from './components/UserCard.jsx'
import UserCardList from './components/UserCardList.jsx'

library.add(faDiagramProject, faRightFromBracket, faUserPen, faTrash, faWandMagicSparkles, faLock, faUser, faCalendar, faUniversity, faMapMarkerAlt, faBriefcase, faTags, faImage, faUsers)


export const AxiosContext = createContext();
export const LoginContext = createContext();
export const API_URL = "http://127.0.0.1:8000";

const client = axios.create({
  baseURL: "http://127.0.0.1:8000",
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  withCredentials: true
});


function App() {
  const navigate = useNavigate();
  const [loginState, setLoginState] = useState({ isLoggedIn: false, userName: null });

  useEffect(() => {
    if (!loginState.isLoggedIn && window.location.pathname !== '/login' && window.location.pathname !== '/signup') {
      navigate('/login');
    }
  }, [loginState, navigate]);

  return (
    <LoginContext.Provider value={{ loginState, setLoginState }}>
      <AxiosContext.Provider value={client}>
        <Routes>
          <Route path="/search" element={<SearchView />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/signup" element={<SignUpForm />} />
          <Route path="/connections" element={<Connections />} />
          <Route path="/suggestions" element={<Suggestions />} />
          <Route path="*" element={<LoginForm/>} />
        </Routes>
      </AxiosContext.Provider>
    </LoginContext.Provider>
  );
}
export default App