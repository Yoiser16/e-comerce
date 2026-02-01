
import requests
import sys

try:
    print("Testing Dashboard Endpoint...")
    response = requests.get('http://localhost:8000/api/v1/dashboard/completo?periodo=7D')
    
    if response.status_code == 200:
        print("✅ Success! Data received.")
        data = response.json()
        print(f"Keys: {list(data.keys())}")
    else:
        print(f"❌ Error {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Connection Failed: {e}")
