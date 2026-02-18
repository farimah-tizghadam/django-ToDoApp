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

⚠️ Important Notes

Migrations must be run before backend or celery

depends_on does not guarantee database readiness

Never run makemigrations inside Docker

Always commit migration files to git

🤖 GitHub Actions

GitHub Actions runs migrations explicitly before tests to avoid schema issues with PostgreSQL and custom user models.
