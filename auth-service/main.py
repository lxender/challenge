import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)