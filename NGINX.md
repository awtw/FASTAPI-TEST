# How to deploy FastAPI with NGINX

OS: Ubuntu 20.04

## Install required packages

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx nginx -y
```

## Increase the limits of client body size
```bash
vim /etc/nginx/nginx.conf

# Add the following line inside the http block
client_max_body_size 500M;
```

## Apply SSL certificate

Take `https://abc.example.com` as an example.
```bash
sudo certbot certonly --nginx -d abc.example.com
```

## Create NGINX configuration file

- HTTP to HTTPS redirection
- HTTPS to `localhost:8000` proxy

```bash
server {
    if ($host = abc.example.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    server_name abc.example.com;
    return 301 https://$host$request_uri;

}

# Server configuration for jue-dui.teamsync.com.tw
server {
    listen 443 ssl http2;
    server_name abc.example.com;
    ssl_certificate /etc/letsencrypt/live/abc.example.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/abc.example.com/privkey.pem; # managed by Certbot

    # Recommended SSL optimizations
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;

    location / {
        proxy_pass http://localhost:8000;
        include /etc/nginx/proxy_params;  # Includes common proxy settings
    }

}
```

