const userAction = async () => {
    var ip = location.host;
    const response = await fetch('http://' + ip + '/movies.json', {
        method: 'POST',
        body: { myBody: "sdfs" },
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    });
    const myJson = await response.json();
}


const login = async () => {
    var ip = location.host;
    var email = document.getElementById("email_login").value;
    var password = document.getElementById("password_login").value;
    const response = await fetch('http://' + ip + '/login', {
        method: 'POST',
        body: 'grant_type=&username=' + email + '&password=' + password + '&scope=&client_id=&client_secret=',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
    const myJson = await response.json();
    localStorage.setItem('access_token', myJson.access_token);

    // Get the user id
    const response2 = await fetch('http://' + ip + '/me', {
        method: 'GET',
        headers: {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    });
    const myJson2 = await response2.json();
    localStorage.setItem('user_id', myJson2.id);
    localStorage.setItem('user_name', myJson2.name);

    // Redirect to the user profile
    window.location.href = "http://" + ip + "/profile/" + myJson2.id;
}


const logout = async () => {
    localStorage.removeItem('access_token');
    window.location.href = "http://" + ip + "/login";
}

const register_user = async () => {
    var ip = location.host;
    var username = document.getElementById("username_register").value;
    var email = document.getElementById("email_register").value;
    var password = document.getElementById("password_register").value;

    const response = await fetch('http://' + ip + '/users', {
        method: 'POST',
        body: JSON.stringify({ name: username, password: password, email: email }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const myJson = await response.json();
    console.log(JSON.stringify(myJson, null, 2));
    if (myJson.id) {
        alert("User created successfully");
        window.location.href = "http://" + ip + "/login";
    }
    else {
        alert("Error creating user");
    }
}
