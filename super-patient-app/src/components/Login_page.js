import 'https://www.w3schools.com/w3css/4/w3.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import reportWebVitals from '../reportWebVitals';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <h1>Hello World!</h1>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();


function loginElement() {
    login_element = (
    <form class="w3-container w3-card-4 w3-light-grey w3-display-left" style="width:30%;margin-left:20%">
        <h2>Login</h2>
        <p>Login with valid credentials.</p>

        <p><label>Username</label>
        <input class="w3-input w3-border w3-round-large" name="username_login" type="text"></input></p>

        <p><label>Password</label>
        <input class="w3-input w3-border w3-round-large" name="password_login" type="text"></input></p>
        <br></br>

        <p><button class="w3-button w3-blue w3-round-large w3-display-bottommiddle" style="margin-bottom:5%;">Login</button></p>
                
    </form>
    );

    return login_element;
};

const loginRoot = ReactDOM.createRoot(document.getElementById('login_root'));
loginRoot.render(<loginElement />);