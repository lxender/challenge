import pytest
from fastapi.testclient import TestClient
from db import get_all_users
from main import app

client = TestClient(app)

sample_user = {
    "email": "testuser@example.com",
    "name": "Test User",
    "password": "password123"
}

sample_login = {
    "email": sample_user["email"],
    "password": sample_user["password"]
}

# Get access_token
def get_token(user=sample_user):
    rows = get_all_users()
    for row in rows:
        print(dict(row))

    response = client.post("/auth/register", json=user)
    if response.status_code == 400:
        response = client.post("/auth/login", json=sample_login)
    data = response.json()
    return data["access_token"]

# /auth/register actually new user
def test_register_new_user():
    response = client.post("/auth/register", json=sample_user)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User created successfully"
    assert "access_token" in data

# /auth/register existing user
def test_register_existing_user():
    response = client.post("/auth/register", json=sample_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

# /auth/login with working credentials
def test_login_success():
    response = client.post("/auth/login", json=sample_login)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Logged in"
    assert "access_token" in data

# /auth/login with wrong credentials
def test_login_invalid_credentials():
    # Wrong password
    response = client.post("/auth/login", json={
        "email": sample_login["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

    # Nonexistent user
    response = client.post("/auth/login", json={
        "email": "doesnotexist@example.com",
        "password": "password123"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

# /profile
def test_profile_endpoint():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/profile", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["profile"]["email"] == sample_user["email"]
    assert data["profile"]["name"] == sample_user["name"]

# /profile/update/{field}
def test_profile_update():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Update name
    new_name = "Updated Test User"
    response = client.post("/profile/update/name", headers=headers, json=new_name)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_name
    assert "hashedPassword" not in data

    # Update email
    new_email = "updateduser@example.com"
    response = client.post("/profile/update/email", headers=headers, json=new_email)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == new_email
    assert "hashedPassword" not in data

    # Reset
    response = client.post("/profile/update/name", headers=headers, json=sample_user["name"])
    response = client.post("/profile/update/email", headers=headers, json=sample_user["email"])


# ----- ADMIN ENDPOINTS -----

# /admin/users
def test_admin_users_list():
    headers = {"Authorization": f"Bearer {get_token()}"}
    response = client.get("/admin/users", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "users" in data

    # Make sure normal user is in the list
    emails = [u["email"] for u in data["users"]]
    assert sample_user["email"] in emails

# /admin/user/{loginId}
def test_admin_user_details():
    headers = {"Authorization": f"Bearer {get_token()}"}
    
    # Get normal user loginId from /admin/users
    users_resp = client.get("/admin/users", headers=headers)
    user_list = users_resp.json()["users"]
    sample_user_id = next(u["loginId"] for u in user_list if u["email"] == sample_user["email"])

    response = client.get(f"/admin/user/{sample_user_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user["email"]

# /admin/create
def test_admin_create_user():
    headers = {"Authorization": f"Bearer {get_token()}"}
    new_user = {"email": "newuser@example.com", "name": "New User", "password": "newpassword"}

    response = client.post("/admin/create", headers=headers, json=new_user)
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

    # Attempt to create same user again -> 400
    response = client.post("/admin/create", headers=headers, json=new_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

# /admin/update
def test_admin_update_user():
    headers = {"Authorization": f"Bearer {get_token()}", "Content-Type": "application/json"}

    # Get user ID to update
    users_resp = client.get("/admin/users", headers=headers)
    user_list = users_resp.json()["users"]

    user_to_update = None
    for user in user_list:
        if user["email"] == "newuser@example.com":
            user_to_update = user
            break

    update_payload = {"loginId": user_to_update["loginId"], "name": "Updated Name"}
    response = client.post("/admin/update", headers=headers, json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

# /admin/delete
def test_admin_delete_user():
    headers = {"Authorization": f"Bearer {get_token()}"}

    # Get user ID to delete
    users_resp = client.get("/admin/users", headers=headers)
    user_list = users_resp.json()["users"]
    user_to_delete = None
    for user in user_list:
        if user["email"] == "newuser@example.com":
            user_to_delete = user
            break

    delete_payload = {"loginId": user_to_delete["loginId"]}
    response = client.post("/admin/delete", headers=headers, json=delete_payload)
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully!"