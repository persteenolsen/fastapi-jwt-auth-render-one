import datetime
import os

import uvicorn
from datetime import datetime, timedelta

from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel, field_validator
from jose import jwt, JWTError

from pydantic import BaseModel


# -----------------------------
# INIT APP
# -----------------------------
app = FastAPI(
    title="FastAPI + JWT + Hosted at Render",
    description="13-05-2026 - Hosted at Render",
    version="1.0.0",
    contact={
        "name": "Per Olsen",
        "url": "https://persteenolsen.netlify.app",
    },
)

# -----------------------------
# ENV
# -----------------------------
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
USERNAME = os.getenv("APP_USERNAME", "admin")
PASSWORD = os.getenv("APP_PASSWORD", "password")


if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing in environment variables")

# -----------------------------
# AUTH
# -----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# -----------------------------
# REQUEST MODELS
# -----------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

# -----------------------------
# ROUTES
# -----------------------------
@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    if form.username != USERNAME or form.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Bad credentials")

    return {
        "access_token": create_token(form.username),
        "token_type": "bearer"
    }

@app.get("/")
def root():
    return {"message": "FastAPI + JWT + Hosted at Render"}

@app.get("/protected")
def protected_route(username: str = Depends(get_user)):
    return {"message": f"Hello, {username}! This is a protected route."}