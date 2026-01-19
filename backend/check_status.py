import requests

BASE_URL = "http://localhost:8000"

def check():
    try:
        auth = requests.post(f"{BASE_URL}/api/auth/login", data={'username': 'admin@univ.edu', 'password': 'Director123!'})
        token = auth.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        resp = requests.get(f"{BASE_URL}/api/examens/?size=100", headers=headers)
        items = resp.json()['items']
        print(f"Total: {len(items)}")
        statuses = set(i['statut'] for i in items)
        print(f"Statuses found: {statuses}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    check()
