
# Wait for the database to be ready
while ! nc -z postgres 5432; do
  echo "Waiting for the database at postgres:5432..."
  sleep 1
done


# Setup the django project

# Database migrations
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL || echo "Superuser already exists."

# Start the server
python3 manage.py runserver 0.0.0.0:8000