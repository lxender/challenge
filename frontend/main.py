import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Use fastapi for the frontend since its used by the main part of the app anyway

app = FastAPI()

PUBLIC = Path("public")
ROUTES = Path("routes")

# Mount subfolders at top-level URLs
app.mount("/styles", StaticFiles(directory=PUBLIC / "styles"), name="styles")
app.mount("/js", StaticFiles(directory=PUBLIC / "js"), name="js")

def load_html(name: str) -> str:
    return (ROUTES / name).read_text(encoding="utf-8")

@app.get("/", response_class=HTMLResponse)
def index():
    return load_html("index.html")


@app.get("/login", response_class=HTMLResponse)
def login():
    return load_html("login.html")


@app.get("/register", response_class=HTMLResponse)
def register():
    return load_html("register.html")


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return load_html("dashboard.html")

@app.get("/admin", response_class=HTMLResponse)
def admin():
    return load_html("admin.html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)