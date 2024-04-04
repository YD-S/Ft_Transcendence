# Setup the django project

# Database migrations
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

# Start the server
python3 manage.py runserver 0.0.0.0:8000