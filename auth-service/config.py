from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
DB_FILE = os.getenv("DB_FILE", "app.db")

ADMIN_LOGIN_ID=os.getenv("ADMIN_LOGIN_ID", 1)