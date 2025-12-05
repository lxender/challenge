import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Form, Response, Depends, Header, Body
from fastapi.middleware.cors import CORSMiddleware

from models import User, LoginUser, ProfileUpdateUser
from db import init_db, get_user_by_email, create_user, update_user
from security import hash_password, verify_password, create_access_token, decode_access_token

init_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# get_current_user be used as a dependency for fastapi routes
# It looks for the "Authorization" header and checks it token for validity
# If the token is valid, it returns the associated user from the database
def get_current_user(authorization: str = Header(...)):
    # Expects the header "Bearer <token>"
    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

@app.post("/auth/register")
def register(user: User):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    create_user(user.email, user.name, hashed)

    # Add user identification to the access token
    access_token = create_access_token({"sub": user.email})

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
    access_token = create_access_token({"sub": loginUser.email})

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
    if field not in ["name", "email", "password"]:
        raise HTTPException(404, detail="Field not allowed to be changed")

    if field == "password":
        hashed = hash_password(value)
        update_user(user["email"], field, hashed)

    update_user(user["email"], field, value)
    # invalidate access token if email changed

    return get_user_by_email(user["email"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)