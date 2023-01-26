import requests

BASE_URL = 'http://192.168.100.10:8000'


def print_response_values(component, response, response_json):
    print(f"{component}: {response} = {response_json}")


def get_all_users():
    print("[Get All Users]: Getting all users...")

    request_headers = {
        "accept": "application/json"
    }

    try:
        #  params as json
        response = requests.get(
            f"{BASE_URL}/api/users", verify=False, headers=request_headers
        )
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")

    # Return request response: status code, output, and user eosb
    print_response_values("[Get All Users]", response, response.json())
    return response, response.json()


def register_new_user(name: str, email: str, avatar: str, password: str):
    print(f"[Register New User]: [{email} , {password}]")

    request_headers = {
        "accept": "application/json"
    }

    json_params = {
        "name": name,
        "email": email,
        "avatar": avatar,
        "password": password
    }

    try:
        #  params as json
        response = requests.post(
            f"{BASE_URL}/api/users", verify=False, headers=request_headers, json=json_params
        )
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")

    # Return request response: status code, output, and user eosb
    print_response_values("[Register New User]", response, response.json())
    return response, response.json()


def login_for_access_token(email: str, password: str):
    print(f"[Login For Access Token]: [{email} , {password}]")
    payload = f"username={email}&password={password}"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}

    try:
        response = requests.post(f"{BASE_URL}/api/login", headers=headers, data=payload, verify=False)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")

    # Return request response: status code
    print_response_values("[Login For Access Token]", response, response.json())
    return response, response.json()


def get_current_user_info(email: str, password: str):
    print(f"[Get User Info]: [{email} , {password}]")

    response, response_json = login_for_access_token(email, password)

    request_headers = {"Authorization": f"Bearer {response_json.get('access_token')}"}

    try:
        #  params as json
        response = requests.get(
            f"{BASE_URL}/api/me", verify=False, headers=request_headers
        )
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")

    # Return request response: status code, output, and user eosb
    print_response_values("[Get User Info]", response, response.json())
    return response, response.json()


def set_user_handles(email: str, password: str, handles: list):
    print(f"[Set User Handles]: [{email} , {password}]")

    response, response_json = login_for_access_token(email, password)

    request_headers = {"Authorization": f"Bearer {response_json.get('access_token')}"}

    info_response, info_response_json = get_current_user_info(email, password)

    json_params = {
        "social_media":
            {
                "TIKTOK": handles[0],
                "FACEBOOK": handles[1],
                "TWITTER": handles[2],
                "LINKEDIN": handles[3],
                "INSTAGRAM": handles[4],
                "YOUTUBE": handles[5],
                "PINTEREST": handles[6],
            }
    }

    try:
        #  params as json
        response = requests.put(
            f"{BASE_URL}/api/users/{info_response_json.get('id')}", verify=False, headers=request_headers, json=json_params
        )
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")

    # Return request response: status code, output, and user eosb
    print_response_values("[Set User Handles]", response, "no JSON")
    return response


def print_all_users(user_list):
    print(f"|================================== Users ==================================")
    for user in user_list:
        print(f"|{user.get('name')}\t {user.get('email')}\t {user.get('id')}")
        social_media = user.get('social_media')
        print(f"\t-TikTok: {social_media.get('TIKTOK')}")
        print(f"\t-Facebook: {social_media.get('FACEBOOK')}")
        print(f"\t-Twitter: {social_media.get('TWITTER')}")
        print(f"\t-Linkedin: {social_media.get('LINKEDIN')}")
        print(f"\t-Instagram: {social_media.get('INSTAGRAM')}")
        print(f"\t-Youtube: {social_media.get('YOUTUBE')}")
        print(f"\t-Pinterest: {social_media.get('PINTEREST')}")
        print(f"|===========================================================================")


if __name__ == "__main__":
    print("Starting Database Initialization...")

    # Get and print current state of DB
    response, response_json = get_all_users()
    print(f"\nFound {len(response_json.get('users'))} Users:")
    # print_all_users(response_json.get('users'))

    total_users = []
    # Attempt to register new users (if already exists nbd, returns 409)
    new_user = ["Nathan Larson", "nathan@secureailabs.com", "pass"]
    new_handles = ["None", "None", "None", "None", "None", "None", "None"]
    total_users.append(new_user)
    reg_response, reg_response_json = register_new_user(new_user[0], new_user[1], "None", new_user[2])
    socials_response = set_user_handles(new_user[1], new_user[2], new_handles)

    new_user = ["Katie Coleman", "katie@gmail.com", "password"]
    new_handles = ["katiekickscancer", "None", "kaydaustin", "None", "katiekickscancer", "katiekickscancer4840", "None"]
    total_users.append(new_user)
    reg_response, reg_response_json = register_new_user(new_user[0], new_user[1], "None", new_user[2])
    socials_response = set_user_handles(new_user[1], new_user[2], new_handles)

    new_user = ["Chris Wark", "chris@gmail.com", "password"]
    new_handles = ["None", "None", "None", "None", "None", "None", "None"]
    total_users.append(new_user)
    reg_response, reg_response_json = register_new_user(new_user[0], new_user[1], "None", new_user[2])
    socials_response = set_user_handles(new_user[1], new_user[2], new_handles)

    response, response_json = get_all_users()
    print_all_users(response_json.get('users'))
    for user in total_users:
        print(f"|{user}")
