FROM python:3.12-bullseye

# Install dependencies
RUN apt-get update && apt-get install -y netcat-traditional nginx

# Set the working directory
WORKDIR /app

COPY . /app

COPY backend-entrypoint.sh /tools/backend-entrypoint.sh
COPY requirements.txt /app/requirements.txt

RUN rm /etc/nginx/sites-enabled/default
COPY nginx/server.conf /etc/nginx/sites-enabled/server.conf
COPY nginx/certs /etc/nginx/ssl

# Install dependencies
RUN pip install -r /app/requirements.txt --break-system-packages --root-user-action ignore


# Expose the port
EXPOSE 443

# Run the app
CMD ["/bin/bash", "/tools/backend-entrypoint.sh"]
