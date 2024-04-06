FROM python:3.12-bullseye

# Install dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# Set the working directory
WORKDIR /app

COPY backend-entrypoint.sh /tools/backend-entrypoint.sh
COPY requirements.txt /app/requirements.txt


# Install dependencies
RUN pip install --break-system-packages -r /app/requirements.txt


# Expose the port
EXPOSE 8000

# Run the app
CMD ["/bin/bash", "/tools/backend-entrypoint.sh"]
