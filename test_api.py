import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    # Test login
    print("🔐 Testing login...")
    login_data = {'username': 'admin', 'password': 'admin123'}
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()['access_token']
            print("✅ Login successful")
            
            headers = {'Authorization': f'Bearer {token}'}
            
            # Test getting projects
            print("\n📁 Testing GET projects...")
            projects_response = requests.get(f"{base_url}/projects", headers=headers)
            if projects_response.status_code == 200:
                projects = projects_response.json()
                print(f"✅ Got {len(projects)} projects")
                for project in projects:
                    print(f"   - {project['name']} (ID: {project['id']})")
            else:
                print(f"❌ Failed to get projects: {projects_response.status_code}")
                return
            
            # Test creating a project
            print("\n➕ Testing POST project...")
            new_project = {
                'name': 'Test Project from API',
                'description': 'This is a test project created via API',
                'status': 'active'
            }
            create_response = requests.post(f"{base_url}/projects", json=new_project, headers=headers)
            if create_response.status_code == 200:
                created_project = create_response.json()
                print("✅ Project created successfully")
                print(f"   Project ID: {created_project['id']}")
                print(f"   Project Name: {created_project['name']}")
                project_id = created_project['id']
            else:
                print(f"❌ Failed to create project: {create_response.status_code}")
                return
            
            # Test creating a task
            print("\n📋 Testing POST task...")
            new_task = {
                'title': 'Test Task from API',
                'description': 'This is a test task created via API',
                'project_id': project_id,
                'priority': 'medium',
                'status': 'todo'
            }
            task_response = requests.post(f"{base_url}/tasks", json=new_task, headers=headers)
            if task_response.status_code == 200:
                created_task = task_response.json()
                print("✅ Task created successfully")
                print(f"   Task ID: {created_task['id']}")
                print(f"   Task Title: {created_task['title']}")
            else:
                print(f"❌ Failed to create task: {task_response.status_code}")
                return
            
            # Test creating a team member
            print("\n👥 Testing POST team member...")
            new_member = {
                'name': 'Test Member from API',
                'email': 'test@example.com',
                'role': 'Developer',
                'department': 'Engineering'
            }
            member_response = requests.post(f"{base_url}/team", json=new_member, headers=headers)
            if member_response.status_code == 200:
                created_member = member_response.json()
                print("✅ Team member created successfully")
                print(f"   Member ID: {created_member['id']}")
                print(f"   Member Name: {created_member['name']}")
            else:
                print(f"❌ Failed to create team member: {member_response.status_code}")
                return
            
            # Test getting updated data
            print("\n🔄 Testing updated data...")
            updated_projects = requests.get(f"{base_url}/projects", headers=headers)
            updated_tasks = requests.get(f"{base_url}/tasks", headers=headers)
            updated_team = requests.get(f"{base_url}/team", headers=headers)
            
            if all(r.status_code == 200 for r in [updated_projects, updated_tasks, updated_team]):
                print("✅ All data retrieved successfully")
                print(f"   Total projects: {len(updated_projects.json())}")
                print(f"   Total tasks: {len(updated_tasks.json())}")
                print(f"   Total team members: {len(updated_team.json())}")
                print("\n🎉 All database operations working correctly!")
            else:
                print("❌ Failed to retrieve updated data")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
