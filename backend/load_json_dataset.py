import requests
import time
import json
import os
from concurrent.futures import ThreadPoolExecutor
import random
import re

MAX_WORKERS = 4

# Configs
JSON_PATH = r"D:\Uni\Term_3\DS\Projs\GraphBasedRecommenderSystem\final-project-Miaad2004\users(999).json"
API_ADDR = "http://127.0.0.1:8000/api/"
PAUSE_ON_EXCEPTION = False
DELAY = 0
DEFAULT_PASS = "123456789aA"
IMAGE_DS_PATH = r"D:\CS\Datasets\celeb\img_align_celeba\img_align_celeba"

# Helpers
def get_random_image_path():
    return os.path.join(IMAGE_DS_PATH, random.choice(os.listdir(IMAGE_DS_PATH)))

def get_username(name):
    name = name.replace(' ', '_').lower()
    name = re.sub(r'[^\w.@+-]', '', name)
    return name

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
    birthday_parts = user['birthday'].split('-')
    birthday_parts[2] = "{:02d}".format(int(birthday_parts[2]))
    user['birthday'] = '-'.join(birthday_parts)
    user['specialties'] = ','.join(user['specialties'])
    user['profile_photo_path'] = get_random_image_path()

    data = {
        'username': user['username'],
        'password': user['password'],
        'birthday': user['birthday'],
        'university': user['university'],
        'specialties': user['specialties'],
        'field': user['field'],
        'workplace': user['workplace']
    }
    
    files = {
        'profile_photo': (os.path.basename(user['profile_photo_path']), open(user['profile_photo_path'], 'rb'), 'image/jpeg')
    }

    # Send request with multipart/form-data
    response = requests.post(f"{API_ADDR}register/", data=data, files=files)
    
    return response

def add_all_users():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(add_user, user) for user in JSON_DATA]
        for i, future in enumerate(futures):
            try:
                response = future.result()
                a = response.json()
                if (response.status_code != 201 and response.status_code != 200) or response.json().get('error') != None:
                    raise Exception(response.text)
                
                print(f"Sample index: {i}, OK")
                
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
    
    if login_response.status_code != 200 or login_response.json()['error'] != None:
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
            
            if response.status_code != 200 or response.json()['error'] != None:
                raise Exception(f"Failed adding connection: {response.text}")
            
            print(f"ID:{user['id']}_to_Id:{connection_ids[i]}-OK")
            
        except Exception as e:
            print(f"Error adding connection from ID:{user['id']} to ID:{connection_ids[i]}")
            print(f"Sample index: {i + 1}")
            print(e)
            
            if PAUSE_ON_EXCEPTION:
                input_ = input("continue?(y,n)")
                if input_.lower() != 'y':
                    break
                
        time.sleep(DELAY)

def add_all_connections():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(login_and_get_token, user) for user in JSON_DATA]
        for i, future in enumerate(futures):
            try:
                token = future.result()
                add_connections_for_user(JSON_DATA[i], token)
                
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
    