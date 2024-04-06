FROM debian:bookworm

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    netcat-traditional

# Set the working directory
WORKDIR /app

COPY tools /tools
COPY Api/requirements.txt /app/requirements.txt


# Install dependencies
RUN pip install --break-system-packages -r /app/requirements.txt


# Expose the port
EXPOSE 8000

# Run the app
CMD ["/bin/bash", "/tools/run.sh"]
