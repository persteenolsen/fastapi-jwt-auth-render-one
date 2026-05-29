# 🚀 FastAPI + Render + Neon PostgreSQL + JWT Authentication (Alembic Ready)

Last updated

- 29-05-2026

A production-ready backend built with FastAPI, PostgreSQL (Neon), JWT authentication, bcrypt password hashing, and Alembic migrations hosted at Render

---

## 🧱 Tech Stack

- FastAPI
- Hosted at Render
- PostgreSQL (Neon)
- SQLAlchemy ORM
- Alembic (migrations)
- JWT Authentication (python-jose)
- bcrypt
- Uvicorn

---

## ✨ Features

- User registration
- Secure password hashing (bcrypt)
- JWT login system
- Protected routes
- PostgreSQL cloud database (Neon)
- Alembic migrations
- Swagger UI testing

---

## 📦 Setup & Installation

### Clone repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

### Create virtual environment
python -m venv .venv

### Activate virtual environment

Windows:
.venv\Scripts\activate

Mac/Linux:
source .venv/bin/activate

### Install dependencies
pip install -r requirements.txt

---

## ⚙️ Environment Variables

Create a `.env` file:

DATABASE_URL=postgresql://USER:PASSWORD@ep-xxx.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

---

## 🗄️ Database (Alembic)

Initialize Alembic:
alembic init alembic

Create migration:
alembic revision --autogenerate -m "create users table"

Apply migration:
alembic upgrade head

---

## 🚀 Run the server

uvicorn app:app --reload

---

## 🌐 API Endpoints

Register user:
POST /register

{
  "email": "user@example.com",
  "password": "12345678"
}

---

Login:
POST /token

username = email
password = password

---

Protected route:
GET /protected

Authorization: Bearer YOUR_TOKEN

---

## 📚 Swagger UI

http://127.0.0.1:8000/docs

---

## 🧠 Architecture

FastAPI → SQLAlchemy → PostgreSQL (Neon)
→ Alembic migrations
→ bcrypt + JWT authentication

---

## 🔐 Security

- bcrypt password hashing
- JWT authentication
- Environment variables
- No hardcoded secrets

---

## ☁️ Deployment Notes

Run before deploy:
alembic upgrade head

Set env vars in Render / production.

---

## 📌 Important

- Do NOT use create_all()
- Always use Alembic migrations
- Neon requires SSL in DATABASE_URL

---

## 📜 License

MIT