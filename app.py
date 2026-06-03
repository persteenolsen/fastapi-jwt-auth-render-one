import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt, JWTError

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel, EmailStr

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import bcrypt

from models import Base, User  # Alembic will manage schema

# -----------------------------
# ENVIRONMENT
# -----------------------------
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing")

# 29-05-2026 - dev mode switch to disable user creation in production
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI(
    title="FastAPI + JWT Auth + Render + PostgreSQL at Neon",
    description="03-06-2026 - FastAPI using JWT Auth hosted at Render using PostgreSQL at Neon as the database",
    version="1.0.0",
    contact={
        "name": "Per Olsen",
        "url": "https://persteenolsen.netlify.app",
    },
)


# -----------------------------
# DATABASE
# -----------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# AUTH (JWT)
# -----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# -----------------------------
# PASSWORDS (bcrypt)
# -----------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


# -----------------------------
# SCHEMAS
# -----------------------------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


# -----------------------------
# ROUTES
# -----------------------------
# Create user route - only for development, disabled in production
@app.post("/register")
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    
    # 🚨 BLOCK IN PRODUCTION
    if not DEV_MODE:
        raise HTTPException(
            status_code=403,
            detail="User creation disabled in production"
        )
    
    existing = db.query(User).filter(User.email == user.email.lower()).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email.lower(),
        hashed_password=hash_password(user.password),
        created_at=datetime.now(timezone.utc),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created (DEV MODE)", "user_id": new_user.id}


@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username.lower()).first()

    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": create_token(user.email),
        "token_type": "bearer",
    }


@app.get("/")
def root():
    return {"message": "FastAPI + Neon + JWT + Alembic ready"}


@app.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"message": f"Hello {user}, you are authenticated"}