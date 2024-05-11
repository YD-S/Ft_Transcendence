# Backend

Pasos a seguir para configurar el backend del proyecto:
- Configurar variables de entorno
- Crear un entorno virtual
- Instalar las dependencias
- Crear y aplicar migraciones
- Crear un superusuario
- Ejecutar el proyecto


```bash
cd Ft_Transcendence/Backend/Api

# Copy and configure the `.env` file
cp env.example .env

# Edit .env file before continuing

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Create a superuser
python3 manage.py createsuperuser

# Run the dev server
python3 manage.py runserver
```

Alternativamente, se puede utilizar Docker para ejecutar el proyecto:

```bash
cd Ft_Transcendence/Backend

# Copy and configure the `.env` file
cp env.example .env

# Edit .env file before continuing
docker build . -t backend:latest
docker run --name backend_container --env-file Api/.env backend:latest
```