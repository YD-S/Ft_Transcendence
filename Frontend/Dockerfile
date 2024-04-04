# Has to be this version of debian because nginx has a specific layout in this version
FROM debian:bullseye

RUN apt-get update
RUN apt-get install -y nginx openssl


COPY . /var/www/frontend
WORKDIR /var/www/frontend
RUN /bin/bash nginx/setup.sh


RUN mkdir -p /etc/nginx/ssl/ && openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj "/CN=neon-pong.com/C=ES/L=Malaga" -keyout /etc/nginx/ssl/neon-pong.key -out /etc/nginx/ssl/neon-pong.crt
RUN mkdir -p /etc/nginx/ssl/ && openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj "/CN=django.neon-pong.com/C=ES/L=Malaga" -keyout /etc/nginx/ssl/django.neon-pong.key -out /etc/nginx/ssl/django.neon-pong.crt

# From nginx:bookworm
CMD ["nginx", "-g", "daemon off;"]