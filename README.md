# Theatre Management API

A RESTful backend application for managing theatres, and reservations, built using a test-driven approach with role-based access control and business-rule–driven updates.

## Features
- Seat capacity management with enforced business rules
- Role-based permissions (admin, manager, customer)
- Token-based authentication
- REST-compliant partial updates
- Fully documented (schema, redoc, swagger)

## Tech Stack
- Python 3.13.5
- Django
- Django REST Framework
- django-allauth
- dj-rest-auth
- SQLite (development)

## Setup

```bash
git clone https://github.com/XCarCedo/theatre-management-api.git
cd theatre-management-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Docs
Docs available at /api/v1/docs/swagger and /api/v1/docs/redoc