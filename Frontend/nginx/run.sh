#!/bin/bash

sed "s/DJANGO_ADMIN_DOMAIN/$DJANGO_ADMIN_DOMAIN/" /var/www/frontend/nginx/server.conf > /tmp/conf
sed "s/DOMAIN/$DOMAIN/" /tmp/conf > /etc/nginx/sites-available/server.conf

cat /etc/nginx/sites-available/server.conf
rm /etc/nginx/sites-enabled/default
ln /etc/nginx/sites-available/server.conf /etc/nginx/sites-enabled/server.conf

nginx -g "daemon off;"