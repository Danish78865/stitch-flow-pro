import requests
import json

def debug_team_api():
    base_url = "http://localhost:8000"
    
    # Login first
    login_data = {'username': 'admin', 'password': 'admin123'}
    login_response = requests.post(f"{base_url}/auth/login", json=login_data)
    
    if login_response.status_code == 200:
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        print("✅ Login successful")
        
        # Test team member creation
        print("\n👥 Testing team member creation...")
        new_member = {
            'name': 'Debug Test Member',
            'email': 'debug@test.com',
            'role': 'Developer',
            'department': 'Engineering'
        }
        
        try:
            response = requests.post(f"{base_url}/team", json=new_member, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Team member created successfully")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"Error details: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            
        # Test getting team members
        print("\n📋 Testing get team members...")
        try:
            response = requests.get(f"{base_url}/team", headers=headers)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                members = response.json()
                print(f"✅ Got {len(members)} team members")
                for member in members:
                    print(f"   - {member['name']} (ID: {member['id']})")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
            
    else:
        print(f"❌ Login failed: {login_response.status_code}")

if __name__ == "__main__":
    debug_team_api()
