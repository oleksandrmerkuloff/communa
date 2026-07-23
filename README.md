# Communa

Communa is a communication and management platform for residential organizations (OSBB / HOA).

The project is currently in MVP stage and is being developed as a modular monolith using Django REST Framework.

## Features

Current implemented modules:

- Authentication (JWT)
- Users
- Organizations
- Membership management
- News system
    - Posts
    - Tags
    - Attachments

Planned modules:

- Petitions
- Role-Based Access Control (RBAC)
- Financial management
- Voting
- Notifications

---

# Tech Stack

Backend

- Python 3.14
- Django 6
- Django REST Framework
- PostgreSQL
- JWT Authentication (SimpleJWT)

Planned

- Docker
- Redis
- Celery

---

# Project Structure

```
core/
    Project configuration

users/
    User model
    Authentication
    Profile management

organization/
    Organization management

membership/
    User memberships
    Organization roles

news/
    Posts
    Tags
    Attachments

petitions/
    (In development)
```

---

# Installation

Clone repository

```bash
git clone <repository_url>

cd communa
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -e .
```

---

# Environment variables

Create `.env`

Example:

```env
SECRET_KEY=your_secret_key

DB_NAME=communa
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

---

# Database

Create migrations

```bash
python manage.py makemigrations
```

Apply migrations

```bash
python manage.py migrate
```

Create superuser

```bash
python manage.py createsuperuser
```

---

# Running

```bash
python manage.py runserver
```

API

```
http://127.0.0.1:8000/
```

Admin

```
http://127.0.0.1:8000/admin/
```

---

# Authentication

Login

```
POST /api/auth/login/
```

Refresh token

```
POST /api/auth/refresh/
```

Logout (Blacklist refresh token)

```
POST /api/auth/logout/
```

---

# API Modules

## Users

```
/api/users/
```

Supports:

- registration
- profile
- update profile
- delete account
- password changing

---

## Organizations

```
/api/organizations/
```

Supports:

- CRUD operations

---

## Memberships

```
/api/memberships/
```

Supports:

- create member
- update member
- remove member
- list organization members

---

## News

```
/api/news/
```

Supports:

- CRUD posts
- CRUD tags
- attachments

---

# Permissions

The project uses custom DRF permissions.

Current role hierarchy:

```
Head
│
Vice Head
│
Accountant
│
Secretary
│
Resident
```

Residents have read-only access.

Higher roles can create and manage content.

RBAC with configurable permissions is planned after MVP.

---

# Tests

Run all tests

```bash
python manage.py test
```

Run module tests

```bash
python manage.py test news
```

---

# Roadmap

Current priority:

- Finish MVP
- Docker support
- Frontend integration

Next phase:

- Petitions
- RBAC
- Refactoring
- Financial module
- Voting

---

# License

Educational / Personal project.

```

---

I would only change two things before committing this:

1. **Add Docker section tomorrow** after you actually create `Dockerfile` and `docker-compose.yml`.
2. Replace

```text
git clone <repository_url>
```

with your actual GitHub repository.

---

Overall, this is exactly the level of README I'd expect from a strong junior or junior+ backend developer delivering an MVP to another teammate. Later, when Communa becomes a public/open-source project or gains external contributors, you can expand it with architecture diagrams, ER diagrams, API documentation, and contribution guidelines.
