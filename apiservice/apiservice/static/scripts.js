const userAction = async () => {
    var ip = location.host;
    const response = await fetch('http://' + ip + '/api/movies.json', {
        method: 'POST',
        body: { myBody: "sdfs" },
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + sessionStorage.getItem('access_token')
        }
    });
    const myJson = await response.json();
}


const login = async () => {
    var ip = location.host;
    var email = document.getElementById("email_login").value;
    var password = document.getElementById("password_login").value;
    const response = await fetch('http://' + ip + '/api/login', {
        method: 'POST',
        body: 'grant_type=&username=' + email + '&password=' + password + '&scope=&client_id=&client_secret=',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
    const myJson = await response.json();
    console.log(JSON.stringify(myJson));
    sessionStorage.setItem('access_token', myJson.access_token);

    // Get the user id
    const response2 = await fetch('http://' + ip + '/api/me', {
        method: 'GET',
        headers: {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + sessionStorage.getItem('access_token')
        }
    });
    const myJson2 = await response2.json();
    sessionStorage.setItem('user_id', myJson2.id);
    sessionStorage.setItem('user_name', myJson2.name);
    sessionStorage.setItem('user_email', myJson2.email);

    // Redirect to the user profile
    window.location.href = "http://" + ip + "/profile/" + myJson2.id;
}


const logout = async () => {
    var ip = location.host;
    clear_session_user_variables();

    window.location.href = "http://" + ip + "/login";
}

const register_user = async () => {
    var ip = location.host;
    var username = document.getElementById("username_register").value;
    var email = document.getElementById("email_register").value;
    var password = document.getElementById("password_register").value;

    const response = await fetch('http://' + ip + '/api/users', {
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


const get_profile_info = async () => {
    var ip = location.host;

    // Get the user id
    const response = await fetch('http://' + ip + '/api/me', {
        method: 'GET',
        headers: {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + sessionStorage.getItem('access_token')
        }
    });

    const myJson = await response.json();
    console.log(JSON.stringify(myJson, null, 2));

    document.getElementById("profile_information").innerHTML = "<h2>Name: " + myJson.name + "</h2>";
    document.getElementById("profile_information").innerHTML += "<h4>Email: " + myJson.email + "</h4>";
}


const get_timeline_data = async () => {
    var ip = location.host;
    console.log("Getting timeline data...")

    let testJsonStr = '{ "timeline" : [' +
        '{ "id":"01" , "user_id":"111345" , "video_path":"Cdata1.mp4" , "video_content_url":"httpstiktok1" , "video_page_url":"httpstiktok.com@handle1" , "timestamp":"1113451" , "datestring":"2023-01-20" , "text":"text here 01" , "summary":"summary here 01" , "title":"Title 1 here" },' +
        '{ "id":"02" , "user_id":"111345" , "video_path":"Cdata2.mp4" , "video_content_url":"httpstiktok2" , "video_page_url":"httpstiktok.com@handle2" , "timestamp":"1113452" , "datestring":"2023-01-21" , "text":"text here 02" , "summary":"summary here 02" , "title":"Title 2 here" },' +
        '{ "id":"03" , "user_id":"111345" , "video_path":"Cdata3.mp4" , "video_content_url":"httpstiktok3" , "video_page_url":"httpstiktok.com@handle3" , "timestamp":"1113453" , "datestring":"2023-01-22" , "text":"text here 03" , "summary":"summary here 03" , "title":"Title 3 here" } ]}';

    const jsonObj = JSON.parse(testJsonStr);
    console.log(jsonObj);

    var timelineHTML = "";
    const timelineObj = jsonObj.timeline;
    let jsonLength = timelineObj.length;
    for (var i = 0; i < jsonLength; i++) {
        timelineHTML += "<button onclick=\"document.getElementById('id" + timelineObj[i].id + "').style.display='block'\" class=\"w3-button w3-blue\" style=\"width:90%\">" + timelineObj[i].title + "</button>";
        timelineHTML += "<div id='id" + timelineObj[i].id + "' class='w3-modal'>";
        timelineHTML += "<div class='w3-modal-content w3-card-4'>";
        timelineHTML += "<header class='w3-container w3-blue'>";
        timelineHTML += "<span onclick=\"document.getElementById('id" + timelineObj[i].id + "').style.display='none'\" class=\"w3-button w3-display-topright\">&times;</span>";
        timelineHTML += "<h2>" + timelineHTML[i].title + "</h2><h5>" + timelineObj[i].datestring + "</h5></header>";
        timelineHTML += "<div class='w3-container'><h4>Text</h4><p>" + timelineObj[i].text + "</p><h4>Summary</h4><p>" + timelineObj[i].summary + "</p>";
        timelineHTML += "</div><footer class='w3-container w3-blue'><h4>Other Data:</h4>";
        timelineHTML += "<p>id: " + timelineObj[i].id + "</p><p>user_id: " + timelineObj[i].user_id + "</p><p>video_path: " + timelineObj[i].video_path + "</p>";
        timelineHTML += "<p>video_content_url: " + timelineObj[i].video_content_url + "</p><p>video_page_url: " + timelineObj[i].video_page_url + "</p><p>timestamp: " + timelineObj[i].timestamp + "</p>";
        timelineHTML += "</footer></div></div><br><br>";
    }

    document.getElementById("timeline_data").innerHTML = timelineHTML;
}


const set_user_handles = async () => {
    var ip = location.host;

    const response = await fetch('http://' + ip + '/api/users/' + sessionStorage.getItem('user_id'), {
        method: 'PUT',
        body: JSON.stringify({
            "social_media":
            {
                TIKTOK: get_document_variable('tiktok_handle'),
                FACEBOOK: get_document_variable('facebook_handle'),
                TWITTER: get_document_variable('twitter_handle'),
                LINKEDIN: get_document_variable('linkedin_handle'),
                INSTAGRAM: get_document_variable('instagram_handle'),
                YOUTUBE: get_document_variable('youtube_handle'),
                PINTEREST: get_document_variable('pinterest_handle')
            }
        }),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + sessionStorage.getItem('access_token')
        }
    });
    if (response.status == 204) {
        alert("User handles Saved. [" + response.status + "]");
    }
    else {
        alert("Error saving user handles: [" + response.status + "]<br>" + JSON.stringify(myJson, null, 2));
    }
}


const get_twitter_feed = async () => {
    var ip = location.host;
    console.log("Getting twitter feed data...")

    // Get the twitter handle from backend API
    const response = await fetch('http://' + ip + '/api/users/' + sessionStorage.getItem('user_id'), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + sessionStorage.getItem('access_token')
        }
    });
    const myJson = await response.json();
    console.log(myJson);
    var twitterHandle = myJson.social_media.TWITTER;
    console.log("Getting twitter feed for username: " + twitterHandle);

    if (twitterHandle == "None") {
        var twitterFeedHTML = "<h1>Invalid Twitter username/handle: {" + twitterHandle + "}";
    } else {
        var twitterFeedHTML = "<a class=\"twitter-timeline\" data-width=\"1000\" data-height=\"600\" href=\"https://twitter.com/" + twitterHandle + "\">Tweets by " + twitterHandle + "</a>";
    }

    document.getElementById("twitter_feed_data").innerHTML = twitterFeedHTML;
    twttr.widgets.load(document.getElementById("twitter_feed_data"));
}

const load_users_page = async () => {
    var ip = location.host;

    // TODO: Hook up /users endpoint
    const response = await fetch('http://' + ip + '/api/users', {
        method: 'GET',
        headers: {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + sessionStorage.getItem('access_token')
        }
    });
    const jsonObj = await response.json();
    console.log("ResponseCode: [" + response.status + "]  JSON: " + JSON.stringify(jsonObj));

    var userlistHTML = "<div class='w3-modal-content'><header class='w3-container w3-blue'>";
    userlistHTML += "<span onclick=\"document.getElementById('user_list_modal').style.display='none'\" class='w3-button w3-display-topright'>&times;</span><h2>User List</h2></header>";
    userlistHTML += "<div class='w3-container'>";
    const userlistObj = jsonObj.users;
    let jsonLength = userlistObj.length;
    for (var i = 0; i < jsonLength; i++) {
        userlistHTML += "<div class='w3-card-4' style='width:25%'><header class='w3-container w3-light-grey'><h3>" + userlistObj[i].name + "</h3></header>";
        userlistHTML += "<div class='w3-container'><p>" + userlistObj[i].email + "<br>" + userlistObj[i].id + "</p><br></div>";
        userlistHTML += "<button class='w3-button w3-block w3-dark-grey'>View Profile</button></div>";
    }
    userlistHTML += "</div><footer class='w3-container w3-blue'><p>Footer</p></div>";

    document.getElementById("user_list_modal").innerHTML = userlistHTML;
    document.getElementById('user_list_modal').style.display = 'block';

    //window.location.href = "http://" + ip + "/users";
}

const logout_and_register = async () => {
    var ip = location.host;

    clear_session_user_variables();

    window.location.href = "http://" + ip + "/register";
}


function get_session_user_variable(item_name) {
    if (sessionStorage.getItem(item_name) == null)
        return "None";
    else
        return sessionStorage.getItem(item_name);
}


function get_document_variable(item_name) {
    if (document.getElementById(item_name) == null)
        return "None";
    else
        return document.getElementById(item_name).value;
}


function clear_session_user_variables() {
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('user_id');
    sessionStorage.removeItem('user_name');
    sessionStorage.removeItem('user_email');
}


setInterval(function () {
    document.getElementById("logged_in_user_box").innerHTML = "<p>Logged in as:</p><p style='font-size:8px';>" +
        get_session_user_variable('user_name') + "<br>" +
        get_session_user_variable('user_email') + "<br>" +
        get_session_user_variable('user_id') + "</p>";
}, 1000);


window.twttr = (function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0],
        t = window.twttr || {};
    if (d.getElementById(id)) return t;
    js = d.createElement(s);
    js.id = id;
    js.src = "https://platform.twitter.com/widgets.js";
    fjs.parentNode.insertBefore(js, fjs);

    t._e = [];
    t.ready = function (f) {
        t._e.push(f);
    };

    return t;
}(document, "script", "twitter-wjs"));
