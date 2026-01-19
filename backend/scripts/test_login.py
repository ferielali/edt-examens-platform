import requests
import json

base_url = "http://localhost:8000"

def test_login(email, password):
    print(f"Testing login for {email}...")
    url = f"{base_url}/api/auth/login"
    data = {
        "username": email,
        "password": password
    }
    try:
        response = requests.post(url, data=data)  # OAuth2 form data
        if response.status_code == 200:
            print("✅ Login SUCCESS")
            print("Token received:", response.json().get("access_token")[:20] + "...")
            return True
        else:
            print(f"❌ Login FAILED: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Test with Director credentials (from fix_passwords.py)
    test_login("admin@univ.edu", "Director123!")
