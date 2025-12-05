from fastapi import Depends, HTTPException, APIRouter, Body
from utils import get_current_user, update_user
from db import get_all_users, get_user_by_id, get_user_by_email, create_user, delete_user
from security import hash_password
from models import User, AdminUserUpdate, AdminUserDelete
from config import ADMIN_LOGIN_ID

def admin_required(user=Depends(get_current_user)):
    if str(user["loginId"]) != str(ADMIN_LOGIN_ID):
        raise HTTPException(401, "Unauthorized")

admin_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(admin_required)]
)

@admin_router.get("/users")
def admin_users_list():
    db_users = get_all_users()
    users = []

    for row in db_users:
        user = dict(row)
        user.pop("hashedPassword", None)
        users.append(user)

    return {
        "users": users
    }

@admin_router.get("/user/{loginId}")
def admin_user_details(loginId: int):
    db_user = get_user_by_id(loginId)
    if db_user is None:
        raise HTTPException(404, detail="User does not exist")
    user = dict(db_user)
    user.pop("hashedPassword", None)
    return user

@admin_router.post("/create")
def admin_create_user(user: User):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    create_user(user.email, user.name, hashed)

    return { "message": "User created successfully" }

@admin_router.post("/update")
def admin_update_user(
    data: AdminUserUpdate
):
    new_data = None
    for key, value in vars(data).items():
        if key != "loginId" and value is not None:
            new_data = (key, value)
            break
    
    if new_data is None:
        raise HTTPException(400, detail="No payload")

    update_user(data.loginId, new_data[0], new_data[1])

    updatedUser = dict(get_user_by_id(data.loginId))
    updatedUser.pop("hashedPassword", None)
    return updatedUser

@admin_router.post("/delete")
def admin_delete_user(data: AdminUserDelete):
    delete_user(data.loginId)

    return { "message": "User deleted successfully!" }