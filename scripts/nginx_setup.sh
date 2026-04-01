#!/usr/bin/env bash
# Run this from the root of the repo

# terminate the script immediately if error occurs
set -e

echo
echo "Creating nginx config file"

sudo tee /etc/nginx/nginx.conf > /dev/null <<'EOF'
events {}

http {
    # VerityBot server
    server {
        listen 80;
        server_name _;

        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name _;

        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;

        ssl_protocols TLSv1.2 TLSv1.3;

        location / {
            proxy_pass https://localhost:5601;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;

            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            proxy_ssl_verify off;
        }
    }
}
EOF

echo
echo "Creating certs for reverse proxy setup..."

sudo mkdir -p /etc/nginx/ssl

sudo openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout /etc/nginx/ssl/nginx.key \
-out /etc/nginx/ssl/nginx.crt \
-subj "/CN=localhost"

sudo nginx -t
sudo systemctl restart nginx