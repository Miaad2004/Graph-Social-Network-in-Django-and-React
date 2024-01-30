import requests
import time
import json

# Configs
JSON_PATH = r"D:\Uni\Term_3\DS\Projs\GraphBasedRecommenderSystem\final-project-Miaad2004\users(99).json"
API_ADDR = "http://127.0.0.1:8000/api/"
PAUSE_ON_EXCEPTION = False
DELAY = 0.01
DEFAULT_PASS = "123456789aA"


def get_username(name):
    parts = name.split(' ')
    return parts[0] if parts else name

def load_json_data(path):
    with open(path, 'r') as f:
        return json.load(f)


# Globals
JSON_DATA = load_json_data(JSON_PATH)
ID_TO_USERNAME = {int(user["id"]): get_username(user["name"]) for user in JSON_DATA}

def send_request(data, endpoint, method="post", token=None):
    url = f"{API_ADDR + endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers['Authorization'] = f'Token {token}'
    
    if method.lower() == "post":
        response = requests.post(url, headers=headers, json=data)
    else:
        response = requests.get(url, headers=headers)
    
    return response


# Add Users
def add_user(user):
    user['username'] = get_username(user['name'])
    user['password'] = DEFAULT_PASS
    user['birthday'] = user.pop('dateOfBirth', None)
    user['university'] = user.pop('universityLocation', None)
    user['birthday'] = user['birthday'].replace('/', '-')
    return send_request(user, "register/")

def add_all_users():
    for i, user in enumerate(JSON_DATA):
        try:
            response = add_user(user)
            if response.status_code != 200:
                raise Exception(response.text)
            
            print(f"{i + 1}-OK")
            
        except Exception as e:
            print(f"Sample index: {i}, Error: {e}")
            
            if PAUSE_ON_EXCEPTION:
                input_ = input("continue?(y,n)")
                if input_.lower() != 'y':
                    break
                
        time.sleep(DELAY)


# Add Connections
def login(username, password):
    data = {"username": username, "password": password}
    return send_request(data, 'login/')

def login_and_get_token(user):
    login_response = login(get_username(user['name']), DEFAULT_PASS)
    
    if login_response.status_code != 200:
        raise Exception(f"Login failed: {login_response.text}")
    
    login_response = json.loads(login_response.text)
    return login_response['token']

def add_connection(target_username, token):
    data = {"username": target_username}
    return send_request(data, 'add_connection/', token=token)

def add_connections_for_user(user, token):
    connection_ids = list(map(int, user['connectionId']))
    connection_usernames = list(map(lambda id: ID_TO_USERNAME[id], connection_ids))
    
    for i, username in enumerate(connection_usernames):
        try:
            response = add_connection(username, token)
            
            if response.status_code != 200:
                raise Exception(f"Failed adding connection: {response.text}")
            
            print(f"ID:{user['id']}_to_Id:{connection_ids[i]}-OK")
            
        except Exception as e:
            print(f"Error adding connection from ID:{user['id']} to ID:{connection_ids[j]}")
            print(f"Sample index: {i + 1}")
            print(e)
            
            if PAUSE_ON_EXCEPTION:
                input_ = input("continue?(y,n)")
                if input_.lower() != 'y':
                    break
                
        time.sleep(DELAY)

def add_all_connections():
    for i, user in enumerate(JSON_DATA):
        try:
            token = login_and_get_token(user)
            add_connections_for_user(user, token)
            
        except Exception as e:
            print(f"Error processing user at index {i}")
            print(e)
            
            if PAUSE_ON_EXCEPTION:
                input_ = input("continue?(y,n)")
                if input_.lower() != 'y':
                    break

# Main
def main():
    add_all_users()
    add_all_connections()

if __name__ == '__main__':
    main()
    