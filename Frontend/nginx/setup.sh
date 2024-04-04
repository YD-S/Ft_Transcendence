#!/bin/bash

cp /var/www/frontend/nginx/server.conf /etc/nginx/sites-available/server.conf
rm /etc/nginx/sites-enabled/default
ln /etc/nginx/sites-available/server.conf /etc/nginx/sites-enabled/server.conf