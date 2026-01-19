import requests
import json
import time

BASE_URL = "http://localhost:8000"

def login():
    try:
        resp = requests.post(f"{BASE_URL}/api/auth/login", 
            data={'username': 'admin@univ.edu', 'password': 'Director123!'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        if resp.status_code == 200:
            return resp.json()['access_token']
        else:
            print(f"Login failed: {resp.status_code} {resp.text}")
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def generate_edt(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'date_debut': '2026-02-15T00:00:00',
        'date_fin': '2026-03-01T00:00:00'
    }
    
    print("Launching generation...")
    start = time.time()
    try:
        resp = requests.post(f"{BASE_URL}/api/examens/generate", 
            json=payload,
            headers=headers,
            timeout=120
        )
        duration = time.time() - start
        print(f"Request took {duration:.2f} seconds")
        
        if resp.status_code == 200:
            print("Success!")
            print(json.dumps(resp.json(), indent=2))
            return True
        else:
            print(f"Generation failed: {resp.status_code}")
            print(resp.text)
            return False
    except Exception as e:
        print(f"Generation error: {e}")
        return False

if __name__ == "__main__":
    token = login()
    if token:
        generate_edt(token)
