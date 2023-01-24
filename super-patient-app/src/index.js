import React from 'react';
import ReactDOM from 'react-dom/client';
//import './index.css';
import { useState } from 'react';
import user from './exampleData/users.json';
import reportWebVitals from './reportWebVitals';
import './w3.css';

/*
  Read local JSON file
*/
function LoadAllUserData() {
  const userStr = JSON.stringify(user);
  const userArr = JSON.parse(userStr);
  let userLength = userArr.length;

  for (var i = 0; i < userLength; i++) {
    console.log(userArr[i].fullname);
  }

  return (
    <React.Fragment>
      <div>
        <button href="#">{userArr[0].fullname}</button>
      </div>
    </React.Fragment>
  );
}
const userDataRoot = ReactDOM.createRoot(document.getElementById('users_list'));
userDataRoot.render(
  <LoadAllUserData />
);


/*
  Load user profile data
*/
function LoadProfileData() {
  const userStr = JSON.stringify(user);
  const userArr = JSON.parse(userStr);
  const katieJson = userArr[0];

  //let userLength = userArr.length;
  //for (var i = 0; i < userLength; i++) {
  //  console.log(userArr[i]);
  //}

  console.log(katieJson)

  return (
    <React.Fragment>
      <div>
        <div className="w3-panel w3-card-4">
          <h3>{katieJson.fullname}</h3>
          <h4>Age: {katieJson.age}</h4>
          <h4>Twitter: {katieJson.twitter_handle}</h4>
          <h4>Youtube: {katieJson.youtube_handle}</h4>
          <h4>TikTok: {katieJson.tiktok_handle}</h4>
        </div>
        <h2>Timeline</h2>
        <div className='w3-panel w3-card-4'>
          <h5>Title: {katieJson.timeline[0].title}</h5>
          <h5>Date: {katieJson.timeline[0].date}</h5>
          <br></br>
          <p>{katieJson.timeline[0].transcript}</p>
        </div>
      </div>
    </React.Fragment>
  );
}
const userProfileRoot = ReactDOM.createRoot(document.getElementById('user_profile'));
userProfileRoot.render(
  <LoadProfileData />
);

/*
  Function to open the profile window populated with user data
*/
function UserProfileActionLink(username) {
  
  const openUserProfilePage = (event) => {
    event.preventDefault();
    console.log("selected button");
  }

  return (
    <button onClick={openUserProfilePage}>
      {username}
    </button>
  )
}


/*
  Generate signup form
*/
function SignupForm() {
  const [inputs, setInputs] = useState({});

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs(values => ({...values, [name]: value}))
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(inputs);
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <label>Enter Your Name: &emsp;
        <input
          type="text" 
          name="fullname"
          value={inputs.fullname || ""} 
          onChange={handleChange}
        />
      </label>
      <hr></hr>
      <label>Enter Your Age: &emsp;
        <input
          type="text" 
          name="age"
          value={inputs.age || ""} 
          onChange={handleChange}
        />
      </label>
      <hr></hr>
      <label>Enter Twitter Handle: &emsp;
        <input
          type="text" 
          name="twitter_handle"
          value={inputs.twitter_handle || ""} 
          onChange={handleChange}
        />
      </label>
      <hr></hr>
      <label>Enter Youtube Handle: &emsp;
        <input
          type="text" 
          name="youtube_handle"
          value={inputs.youtube_handle || ""} 
          onChange={handleChange}
        />
      </label>
      <hr></hr>
      <label>Enter TikTok Handle: &emsp;
        <input
          type="text" 
          name="tiktok_handle"
          value={inputs.tiktok_handle || ""} 
          onChange={handleChange}
        />
      </label>
      <hr></hr>
      <input type="submit" />
    </form>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <SignupForm />
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
