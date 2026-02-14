# django-ToDoApp
> simple ToDoApp with django class based view

### Features
* Django LTS
* Class Based
* User authentication
* Black
* Flake8
* Responsive Design
* Bootstrap5




🐳 Django + Docker + PostgreSQL (Stage / CI Setup)

This project uses PostgreSQL instead of SQLite and runs inside Docker with Celery and GitHub Actions support.

📁 Project Structure </br>
repo/ </br>
├── core/  </br>
│   ├── manage.py  </br>
│   ├── accounts/  </br>
│   ├── todo/  </br>
│   ├── core/  </br>
│   │   ├── settings.py  </br>
│   │   ├── wsgi.py  </br>
│   │   ├── celery.py  </br>
├── docker-compose-stage.yml  </br>
├── Dockerfile


manage.py → core/manage.py

Django project package → core/core/

Custom user model → accounts.User

🛢 Database Configuration (PostgreSQL)

In settings.py:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": "5432",
    }
}

🐋 Dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

▶️ How to Run (Stage / Local)
docker compose -f docker-compose-stage.yml down -v
docker compose -f docker-compose-stage.yml up -d postgres redis
docker compose -f docker-compose-stage.yml run --rm migrate
docker compose -f docker-compose-stage.yml up -d backend worker beater nginx

⚠️ Important Notes

Migrations must be run before backend or celery

depends_on does not guarantee database readiness

Never run makemigrations inside Docker

Always commit migration files to git

🤖 GitHub Actions

GitHub Actions runs migrations explicitly before tests to avoid schema issues with PostgreSQL and custom user models.
