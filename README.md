# Communa

Communa is a backend platform for Homeowners Associations (HOAs / ОСББ) that provides a centralized system for managing organizations, members, news, and petitions.

This repository contains the MVP version of the project built with Django REST Framework.

---

# Features

## Authentication

* JWT Authentication
* Access & Refresh Tokens
* Token Rotation
* Token Blacklisting
* Custom User Model

## Organizations

* Create organizations
* Retrieve organization information
* Update organization data
* Delete organizations

## Membership

* Join organization
* Member management
* Role system (MVP)

  * Head
  * Resident

## News

* Create news
* Update news
* Delete news
* Tags
* Attachments
* Draft / Published / Archived statuses

## Petitions

* Create petitions
* Retrieve petitions
* Update petitions
* Delete petitions

---

# Technology Stack

* Python 3.14
* Django 6
* Django REST Framework
* PostgreSQL
* Docker
* JWT (SimpleJWT)

---

# Project Structure

```
core/
users/
organization/
membership/
news/
petitions/

manage.py
Dockerfile
docker-compose.yml
pyproject.toml
```

---

# Running with Docker

## 1. Clone repository

```bash
git clone <repository_url>
cd communa
```

## 2. Create environment file

Create a `.env` file based on `.env.example`.

Example:

```env
SECRET_KEY=your_secret_key

DB_NAME=communa-db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

## 3. Build containers

```bash
docker compose up --build
```

Django will automatically:

* apply migrations
* collect static files
* start the development server

---

# Development Server

```
http://localhost:8000/
```

Admin:

```
http://localhost:8000/admin/
```

---

# Running Tests

```bash
docker compose run --rm web python manage.py test
```

or locally

```bash
python manage.py test
```

---

# API Authentication

Obtain JWT tokens:

```
POST /api/token/
```

Refresh token:

```
POST /api/token/refresh/
```

Logout (blacklist refresh token):

```
POST /api/token/logout/
```

---

# Current MVP Modules

* Users
* Organizations
* Membership
* News
* Petitions

---

# Planned Features

The project will continue development after the MVP.

Planned features include:

* Role-Based Access Control (RBAC)
* Voting System
* Financial Management
* Redis
* Celery
* Email Notifications
* OpenAPI / Swagger Documentation
* CI/CD
* Production Deployment
* Microservice migration (when necessary)

---

# License

This project is currently intended for educational and portfolio purposes.
