import requests
import time
import json

def get_username(name):
    return name.split(' ')[0]

PAUSE_ON_EXCEPTION = False
DELAY = 0.01
API_ADDR = "http://127.0.0.1:8000/api/"
JSON_PATH = r"D:\Uni\Term_3\DS\Projs\GraphBasedRecommenderSystem\final-project-Miaad2004\users(99).json"
DEFAULT_PASS = "123456789aA"

with open(JSON_PATH, 'r') as f:
    JSON_DATA = json.load(f)
    
ID_TO_USERNAME = {int(user["id"]): get_username(user["name"]) for user in JSON_DATA}

    
def add_user(data, endpoint="register/"):
    url = f"{API_ADDR + endpoint}"
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, json=data)
    
    return response

def add_all_users():
    for i, user in enumerate(JSON_DATA):
        
        user['username'] = get_username(user['name'])
        user['password'] = DEFAULT_PASS
        
        # camel_case to snake_case
        user['date_of_birth'] = user.pop('dateOfBirth', None)
        user['university_location'] = user.pop('universityLocation', None)
        
        user['date_of_birth'] = user['date_of_birth'].replace('/', '-')
        
        try:
            response = add_user(user)
            if response.status_code != 201:
                raise Exception(response.text)
            
            print(f"{i + 1}-OK")
        
        except Exception as e:
            print(f"Sample index: {i}")
            print(e)
            
            if PAUSE_ON_EXCEPTION:
                input_ = input("continue?(y,n)")
                if input_.lower() != 'y':
                    break
        
        time.sleep(DELAY)

def login(username, password, endpoint='login/'):
    url = f"{API_ADDR + endpoint}"
    headers = {"Content-Type": "application/json"}
    data = {"username": username, "password": password}
    
    response = requests.post(url, headers=headers, json=data)
    
    return response

def add_connection(target_username, token, endpoint='add_connection/'):
    url = f"{API_ADDR + endpoint}"
    headers = {"Content-Type": "application/json", 'Authorization': f'Token {token}'}
    data = {"username": target_username}
    
    response = requests.post(url, headers=headers, json=data)
    
    return response

def add_all_connections():
    for i, user in enumerate(JSON_DATA):
        login_response = login(get_username(user['name']), DEFAULT_PASS)
        if login_response.status_code != 200:
            raise Exception(login_response.text)
        
        login_response = json.loads(login_response.text)
        token = login_response['token']
        
        connection_ids = list(map(int, user['connectionId']))
        connection_usernames = list(map(lambda id: ID_TO_USERNAME[id], connection_ids))
        
        
        for j, username in enumerate(connection_usernames):
            try:
                response = add_connection(username, token)
                
                if response.status_code != 201:
                    raise Exception(response.text)
            
                print(f"ID:{user["id"]}_to_Id:{connection_ids[j]}-OK")
        
            
            except Exception as e:
                print(f"ID:{user["id"]}_to_Id:{connection_ids[j]}-OK")
                print(f"Sample index: {i + 1}")
                print(e)
            
                if PAUSE_ON_EXCEPTION:
                    input_ = input("continue?(y,n)")
                    if input_.lower() != 'y':
                        break
        
            time.sleep(DELAY)
        

def main():
    add_all_users()
    add_all_connections()
    



if __name__ == '__main__':
    main()
    