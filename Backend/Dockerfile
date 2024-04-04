FROM debian:bookworm

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

# Create a directory for the app \
COPY Api /app
COPY tools /tools

# Set the working directory
WORKDIR /app

# Install dependencies
## Create a virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
## Install the dependencies
RUN pip install -r requirements.txt


# Expose the port
EXPOSE 8000

# Run the app
CMD ["/bin/bash", "/tools/run.sh"]
