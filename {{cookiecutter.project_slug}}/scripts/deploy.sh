#!/bin/bash
#
# Deployment script for {{ cookiecutter.project_name }}
#
# Usage: ./deploy.sh [environment]
# Example: ./deploy.sh production

set -e

# Configuration
PROJECT_NAME="{{ cookiecutter.project_slug }}"
PROJECT_DIR="/home/app/${PROJECT_NAME}"
VENV_DIR="${PROJECT_DIR}/.venv"
REPO_URL="git@github.com:yourusername/${PROJECT_NAME}.git"
BRANCH="main"
ENVIRONMENT="${1:-production}"

echo "Deploying ${PROJECT_NAME} to ${ENVIRONMENT}..."

# Create project directory if it doesn't exist
sudo mkdir -p ${PROJECT_DIR}
sudo chown app:app ${PROJECT_DIR}

# Switch to app user
sudo -u app bash << EOF
    cd ${PROJECT_DIR}
    
    # Clone or pull latest code
    if [ ! -d ".git" ]; then
        git clone ${REPO_URL} .
    else
        git fetch origin
        git reset --hard origin/${BRANCH}
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "${VENV_DIR}" ]; then
        python3 -m venv ${VENV_DIR}
    fi
    
    # Activate virtual environment
    source ${VENV_DIR}/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    pip install -r requirements/production.txt
    
    # Copy environment file
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo "Please edit .env file with production settings!"
    fi
    
    # Collect static files
    cd ${PROJECT_NAME}
    python manage.py collectstatic --noinput
    
    # Run migrations
    python manage.py migrate --noinput
    
    # Create cache table
    python manage.py createcachetable || true
    
    # Compile translations
    python manage.py compilemessages || true
EOF

# Reload systemd and restart services
sudo systemctl daemon-reload
sudo systemctl enable ${PROJECT_NAME}
sudo systemctl restart ${PROJECT_NAME}

# If using Celery
if grep -q "USE_CELERY=True" ${PROJECT_DIR}/.env; then
    sudo systemctl enable ${PROJECT_NAME}-celery
    sudo systemctl restart ${PROJECT_NAME}-celery
    sudo systemctl enable ${PROJECT_NAME}-celery-beat
    sudo systemctl restart ${PROJECT_NAME}-celery-beat
fi

# Reload nginx
sudo nginx -t && sudo systemctl reload nginx

echo "Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Edit ${PROJECT_DIR}/.env with production settings"
echo "2. Create superuser: cd ${PROJECT_DIR}/${PROJECT_NAME} && ${VENV_DIR}/bin/python manage.py createsuperuser"
echo "3. Check service status: sudo systemctl status ${PROJECT_NAME}"
echo "4. View logs: sudo journalctl -u ${PROJECT_NAME} -f"