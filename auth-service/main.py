import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Form, Response, Depends, Header, Body
from fastapi.middleware.cors import CORSMiddleware

from models import User, LoginUser, ProfileUpdateUser
from db import init_db, get_user_by_email, get_user_by_id, create_user
from security import hash_password, verify_password, create_access_token, decode_access_token
from utils import get_current_user, update_user
from admin import admin_router

init_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)


@app.post("/auth/register")
def register(user: User):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    create_user(user.email, user.name, hashed)
    dbUser = get_user_by_email(user.email)

    # Add user identification to the access token
    access_token = create_access_token({"sub": str(dbUser["loginId"])})

    return {
        "message": "User created successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/auth/login")
def login(res: Response, loginUser: LoginUser):
    dbUser = get_user_by_email(loginUser.email)
    if not dbUser or not verify_password(loginUser.password, dbUser["hashedPassword"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Add user identification to the access token
    access_token = create_access_token({"sub": str(dbUser["loginId"])})

    return {
        "message": "Logged in",
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/profile")
def profile(user=Depends(get_current_user)):
    return {
        "profile": {
            "email": user["email"],
            "name": user["name"]
        }
    }

@app.post("/profile/update/{field}")
def profile_update(
    field: str,
    value: str = Body(...),
    user=Depends(get_current_user)
):
    update_user(user["loginId"], field, value)
    updatedUser = dict(get_user_by_id(user["loginId"]))
    updatedUser.pop("hashedPassword", None)
    return updatedUser
