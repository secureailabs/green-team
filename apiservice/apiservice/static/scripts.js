
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


const get_profile_info = async () => {
    var ip = location.host;

    // Get the user id
    const response = await fetch('http://' + ip + '/me', {
        method: 'GET',
        headers: {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
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
    var twitterHandle = document.getElementById("twitter_handle").value;
    var youtubeHandle = document.getElementById("youtube_handle").value;
    var tiktokHandle = document.getElementById("tiktok_handle").value;
    /*
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
    */
    console.log("Twitter: " + twitterHandle);
    console.log("Youtube: " + youtubeHandle);
    console.log("TikTok: " + tiktokHandle);
}
