# Bravo-Team
Shallion shopping system

# Django Project Setup

A clean Django project with basic configuration.

## Requirements

- Python 3.12+
- PostgreSQL (optional, can use SQLite for development)

## Setup

1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements/develop.txt  # For development
pip install -r requirements/production.txt  # For production
```

4. Create .env file
```bash
cp .env.example .env
```

5. Run migrations
```bash
python manage.py migrate
```

7. Create superuser (optional)
```bash
python manage.py createsuperuser
```

8. Run development server
```bash
python manage.py runserver
```

## Project Structure

```
├── apps/
│   └── common/
├── core/
│   ├── settings/
│   │   ├── base.py
│   │   ├── develop.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── static/
├── staticfiles/
├── media/
├── requirements/
│   ├── base.txt
│   ├── develop.txt
│   └── production.txt
└── manage.py
```

## Development

- Use `python manage.py runserver` to run development server
- Access admin panel at `http://localhost:8000/admin/`


