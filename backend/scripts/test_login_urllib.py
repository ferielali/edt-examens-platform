import urllib.request
import urllib.parse
import json
import ssl

# Ignore SSL errors for localhost
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = "http://localhost:8000"

def test_login(email, password):
    print(f"Testing login for {email}...")
    url = f"{base_url}/api/auth/login"
    data = urllib.parse.urlencode({
        "username": email,
        "password": password
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, method="POST")
    # Content-Type is application/x-www-form-urlencoded by default for urlencoded data
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            if response.status == 200:
                body = response.read().decode("utf-8")
                token = json.loads(body).get("access_token")
                print("✅ Login SUCCESS")
                print("Token received:", token[:20] + "...")
                return True
            else:
                print(f"❌ Login FAILED: {response.status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"❌ Login FAILED: {e.code}")
        print(e.read().decode("utf-8"))
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Test with Director credentials (from fix_passwords.py)
    test_login("admin@univ.edu", "Director123!")
