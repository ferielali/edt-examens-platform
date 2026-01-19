import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = "http://localhost:8000"

def run_test():
    # 1. Login
    print("1️⃣ Testing Login...")
    login_url = f"{base_url}/api/auth/login"
    data = urllib.parse.urlencode({
        "username": "admin@univ.edu",
        "password": "Director123!"
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(login_url, data=data, method="POST")
        with urllib.request.urlopen(req, context=ctx) as response:
            if response.status != 200:
                print("❌ Login Failed")
                return
            body = json.loads(response.read().decode("utf-8"))
            token = body.get("access_token")
            print("✅ Login Success")
            
    except Exception as e:
        print(f"❌ Login Error: {e}")
        return

    # 2. Access Dashboard (Protected)
    print("\n2️⃣ Testing Dashboard Access...")
    stats_url = f"{base_url}/api/dashboard/stats"
    req = urllib.request.Request(stats_url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            if response.status == 200:
                print("✅ Dashboard Access Success")
                data = json.loads(response.read().decode("utf-8"))
                print(f"   Stats: {data}")
            else:
                print(f"❌ Dashboard Failed: {response.status}")
    except Exception as e:
        print(f"❌ Dashboard Error: {e}")

    # 3. Forgot Password Request
    print("\n3️⃣ Testing Forgot Password...")
    reset_url = f"{base_url}/api/auth/request-reset"
    json_data = json.dumps({"email": "admin@univ.edu"}).encode("utf-8")
    req = urllib.request.Request(reset_url, data=json_data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            if response.status == 200:
                print("✅ Forgot Password Request Success")
                data = json.loads(response.read().decode("utf-8"))
                print(f"   Response: {data}")
            else:
                print(f"❌ Forgot Password Failed: {response.status}")
    except Exception as e:
        print(f"❌ Forgot Password Error: {e}")

if __name__ == "__main__":
    run_test()
