import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Form, Response
from fastapi.middleware.cors import CORSMiddleware

from db import init_db, get_user_by_email, create_user
from security import hash_password, verify_password, create_access_token

init_db()

class LoginUser(BaseModel):
    email: str
    password: str

class RegisterUser(BaseModel):
    email: str
    name: str
    password: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/register")
def register(registerUser: RegisterUser):
    if get_user_by_email(registerUser.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(registerUser.password)
    create_user(registerUser.email, registerUser.name, hashed)

    access_token = create_access_token({"sub": email})

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

    access_token = create_access_token({"sub": loginUser.email})

    return {
        "message": "Logged in",
        "access_token": access_token,
        "token_type": "bearer"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)