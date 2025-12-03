import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Use fastapi for the frontend since its used by the main part of the app anyway

app = FastAPI()

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)