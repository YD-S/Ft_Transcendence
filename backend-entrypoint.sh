
# Ensure $POSTGRES_HOST is set
if [ -z "$POSTGRES_HOST" ]; then
  POSTGRES_HOST="postgres"
fi

# Wait for the database to be ready
while ! nc -z $POSTGRES_HOST 5432; do
  echo "Waiting for the database at $POSTGRES_HOST:5432..."
  sleep 1
done


# Setup the django project

# Database migrations
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL" || echo "Superuser already exists."

# Start nginx
nginx -g "daemon off;" &

# Start the server
DJANGO_SETTINGS_MODULE=NeonPong.settings daphne -e ssl:8000:privateKey=/etc/nginx/ssl/neon-pong.com.key:certKey=/etc/nginx/ssl/neon-pong.com.crt NeonPong.asgi:application
