import requests
import json

BASE_URL = "http://localhost:8000"

def login():
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/login", 
            data={'username': 'admin@univ.edu', 'password': 'Director123!'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        if resp.status_code == 200:
            return resp.json()['access_token']
        return None
    except:
        return None

def check_salles(token):
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(f"{BASE_URL}/api/dashboard/salles", headers=headers)
    if resp.status_code == 200:
        rooms = resp.json()
        print(f"Total rooms: {len(rooms)}")
        types = set(r.get('type') for r in rooms)
        print(f"Room types found: {types}")
        # Print a sample room
        if rooms:
            print("Sample room:", json.dumps(rooms[0], indent=2))
            
if __name__ == "__main__":
    token = login()
    if token:
        check_salles(token)
