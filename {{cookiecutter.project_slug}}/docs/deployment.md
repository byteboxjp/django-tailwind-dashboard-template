# Deployment Guide

This guide covers deploying {{ cookiecutter.project_name }} to a production environment.

## Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Python {{ cookiecutter.python_version }}+
- PostgreSQL {{ cookiecutter.postgresql_version }}+
- Redis (if using Celery)
- Nginx
- SSL certificate (Let's Encrypt recommended)

## Server Setup

### 1. System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib \
    redis-server \
    nginx \
    certbot python3-certbot-nginx \
    build-essential libpq-dev
```

### 2. PostgreSQL Setup

```bash
# Create database and user
sudo -u postgres psql

CREATE DATABASE {{ cookiecutter.project_slug }}_db;
CREATE USER {{ cookiecutter.project_slug }}_user WITH PASSWORD 'your-secure-password';
ALTER ROLE {{ cookiecutter.project_slug }}_user SET client_encoding TO 'utf8';
ALTER ROLE {{ cookiecutter.project_slug }}_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE {{ cookiecutter.project_slug }}_user SET timezone TO '{{ cookiecutter.timezone }}';
GRANT ALL PRIVILEGES ON DATABASE {{ cookiecutter.project_slug }}_db TO {{ cookiecutter.project_slug }}_user;
\q
```

### 3. Create Application User

```bash
# Create app user
sudo useradd -m -s /bin/bash app
sudo usermod -aG sudo app
```

## Application Deployment

### 1. Initial Deployment

```bash
# Run deployment script
sudo -u app bash
cd /home/app
git clone https://github.com/yourusername/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}
chmod +x scripts/deploy.sh
./scripts/deploy.sh production
```

### 2. Environment Configuration

Edit the `.env` file with production settings:

```bash
cd /home/app/{{ cookiecutter.project_slug }}
nano .env
```

Key settings to update:
- `SECRET_KEY` - Generate a new secret key
- `ALLOWED_HOSTS` - Your domain name
- Database credentials
- Email settings
- Redis settings (if using)
- Turnstile keys (if using)

### 3. Nginx Configuration

```bash
# Copy nginx config
sudo cp /home/app/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}/config/nginx.conf \
    /etc/nginx/sites-available/{{ cookiecutter.project_slug }}

# Enable site
sudo ln -s /etc/nginx/sites-available/{{ cookiecutter.project_slug }} \
    /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 4. SSL Certificate

```bash
# Obtain certificate with Certbot
sudo certbot --nginx -d {{ cookiecutter.domain_name }} -d www.{{ cookiecutter.domain_name }}
```

### 5. Systemd Services

```bash
# Copy service files
sudo cp /home/app/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}/config/systemd/*.service \
    /etc/systemd/system/

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable {{ cookiecutter.project_slug }}
sudo systemctl start {{ cookiecutter.project_slug }}

# If using Celery
sudo systemctl enable {{ cookiecutter.project_slug }}-celery
sudo systemctl start {{ cookiecutter.project_slug }}-celery
sudo systemctl enable {{ cookiecutter.project_slug }}-celery-beat
sudo systemctl start {{ cookiecutter.project_slug }}-celery-beat
```

## Post-Deployment

### Create Superuser

```bash
cd /home/app/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}
source ../.venv/bin/activate
python manage.py createsuperuser
```

### Check Service Status

```bash
# Application
sudo systemctl status {{ cookiecutter.project_slug }}
sudo journalctl -u {{ cookiecutter.project_slug }} -f

# Celery (if using)
sudo systemctl status {{ cookiecutter.project_slug }}-celery
sudo journalctl -u {{ cookiecutter.project_slug }}-celery -f
```

## Monitoring

### Application Logs

```bash
# Django logs
tail -f /home/app/{{ cookiecutter.project_slug }}/logs/django.log

# Nginx logs
tail -f /var/log/nginx/{{ cookiecutter.project_slug }}_access.log
tail -f /var/log/nginx/{{ cookiecutter.project_slug }}_error.log
```

### Health Checks

- Application: `https://{{ cookiecutter.domain_name }}/health/` (if implemented)
- Admin: `https://{{ cookiecutter.domain_name }}/admin/`

## Updates

To deploy updates:

```bash
cd /home/app/{{ cookiecutter.project_slug }}
./scripts/deploy.sh production
```

## Backup

### Database Backup

```bash
# Create backup
pg_dump -U {{ cookiecutter.project_slug }}_user -h localhost {{ cookiecutter.project_slug }}_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
psql -U {{ cookiecutter.project_slug }}_user -h localhost {{ cookiecutter.project_slug }}_db < backup_20240101_120000.sql
```

### Media Files Backup

```bash
# Backup media files
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz /home/app/{{ cookiecutter.project_slug }}/media/
```

## Security Checklist

- [ ] Change default `SECRET_KEY`
- [ ] Set strong database password
- [ ] Configure firewall (ufw)
- [ ] Disable root SSH login
- [ ] Set up fail2ban
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity
- [ ] Set up automated backups
- [ ] Configure Sentry for error tracking

## Troubleshooting

### Application won't start

```bash
# Check logs
sudo journalctl -u {{ cookiecutter.project_slug }} -n 100

# Check syntax
cd /home/app/{{ cookiecutter.project_slug }}/{{ cookiecutter.project_slug }}
source ../.venv/bin/activate
python manage.py check --deploy
```

### Static files not loading

```bash
# Recollect static files
python manage.py collectstatic --noinput

# Check nginx config
sudo nginx -t
```

### Database connection errors

```bash
# Test database connection
psql -U {{ cookiecutter.project_slug }}_user -h localhost -d {{ cookiecutter.project_slug }}_db

# Check PostgreSQL status
sudo systemctl status postgresql
```