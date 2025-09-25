# Unilink Server (Django + DRF)

A social backend built with Django REST Framework, JWT auth, and PostgreSQL.

## Prerequisites

- Python 3.11+
- PostgreSQL 13+
- pip, venv (recommended)

## Quick Start

```bash
# 1) Clone
git clone https://github.com/hyperingenious/unilink-server.git
cd unilink-server

# 2) Create & activate venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Create PostgreSQL database and user
# Adjust values if needed
psql -U postgres -c "CREATE USER user_unilink WITH PASSWORD 'unilink_password';"
psql -U postgres -c "CREATE DATABASE unilink_db OWNER user_unilink;"

# 5) Apply migrations
python manage.py migrate

# 6) Run server
python manage.py runserver 0.0.0.0:8000
```

Server will be available at `http://127.0.0.1:8000/`.

## Configuration

All key settings live in `unilink/settings.py`.

- `DATABASES`: Default points to local PostgreSQL `unilink_db` with user `user_unilink`.
- `REST_FRAMEWORK`:
  - `DEFAULT_AUTHENTICATION_CLASSES`: `rest_framework_simplejwt.authentication.JWTAuthentication`
  - `DEFAULT_PERMISSION_CLASSES`: `rest_framework.permissions.IsAuthenticated`
- `SIMPLE_JWT`: Token lifetimes (access 7d, refresh 30d by default).

If you change DB credentials, update `DATABASES` accordingly.

## Apps

- `users`: Auth, registration, login, email verification, profiles
- `social`: Posts, comments, followers, reactions, feed, search

## Running Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create Superuser (optional)

```bash
python manage.py createsuperuser
```

Admin available at `http://127.0.0.1:8000/admin/`.

## License

MIT
