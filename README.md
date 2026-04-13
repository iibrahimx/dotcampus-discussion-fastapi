# Dot Campus Discussion API

A secure RESTful API for the Dot Campus Learning Community built with FastAPI.

## Features

- User signup and login
- JWT authentication
- Role-based access control
- Roles: admin, mentor, learner
- CRUD operations for discussions
- Comments on discussions
- Admin role management and user deletion
- Interactive API docs with Swagger

---

## Roles and Permissions

### Learner

- View all discussions
- View a single discussion
- Create a discussion
- Update own discussion
- Delete own discussion
- View comments on a discussion
- Comment on a discussion

### Mentor

- Everything a learner can do
- Update any discussion

### Admin

- Everything a mentor can do
- Delete any discussion
- Delete any comment
- Change user roles between learner and mentor
- Delete any user account

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT
- Passlib
- Pytest

---

## Project Structure

```bash
dotcampus-discussion-fastapi/
├── app/
│   ├── routers/
│   │   ├── admin.py
│   │   ├── comments.py
│   │   ├── discussions.py
│   │   └── users.py
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── permissions.py
│   └── schemas.py
├── tests/
├── README.md
└── requirements.txt
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/iibrahimx/dotcampus-discussion-fastapi.git
cd dotcampus-discussion-fastapi
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a .env file and add:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/dotcampus_fastapi_db
SECRET_KEY=supersecretkey123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

- Swagger UI: http://127.0.0.1:8000/docs

---

## Testing

Run tests with:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## Database Design

**DB diagram link:** [Db diagram](https://dbdiagram.io/d/697fe6dfbd82f5fce247cdae)

---

## Deployment

**Live API link:** Live API
