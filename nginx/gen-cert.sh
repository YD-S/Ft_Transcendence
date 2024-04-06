#!/bin/bash
mkdir -p certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -subj "/CN=$1/C=ES/L=Malaga" -keyout certs/"$1.key" -out certs/"$1.crt"