#!/usr/bin/env python
"""Post-generation cookiecutter hook."""
import os
import shutil
import subprocess
import sys

def remove_file(filepath):
    """Remove a file if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)

def remove_dir(dirpath):
    """Remove a directory if it exists."""
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

def run_command(command, error_message):
    """Run a shell command and handle errors."""
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {error_message}")
        print(f"Output: {e.stdout.decode()}")
        print(f"Error: {e.stderr.decode()}")
        sys.exit(1)

# Check if we need to remove optional features
USE_CELERY = "{{ cookiecutter.use_celery }}" == "y"
USE_REDIS = "{{ cookiecutter.use_redis }}" == "y"
USE_SENTRY = "{{ cookiecutter.use_sentry }}" == "y"
USE_CLOUDFLARE_TURNSTILE = "{{ cookiecutter.use_cloudflare_turnstile }}" == "y"
DATABASE_ENGINE = "{{ cookiecutter.database_engine }}"

# Remove Celery files if not needed
if not USE_CELERY:
    remove_file("{{ cookiecutter.project_slug }}/config/celery.py")
    remove_file("{{ cookiecutter.project_slug }}/apps/core/tasks.py")
    print("✓ Removed Celery configuration (not selected)")

# Update settings if SQLite is selected
if DATABASE_ENGINE == "sqlite3":
    settings_file = "{{ cookiecutter.project_slug }}/config/settings/base.py"
    with open(settings_file, "r") as f:
        content = f.read()
    
    # Replace PostgreSQL config with SQLite
    content = content.replace(
        """DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_NAME", "{{ cookiecutter.project_slug }}_db"),
        "USER": os.getenv("POSTGRES_USER", "{{ cookiecutter.project_slug }}_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}""",
        """DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}"""
    )
    
    with open(settings_file, "w") as f:
        f.write(content)
    print("✓ Configured SQLite database")

# Create necessary directories
directories = [
    "{{ cookiecutter.project_slug }}/media",
    "{{ cookiecutter.project_slug }}/staticfiles",
    "{{ cookiecutter.project_slug }}/logs",
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    # Create .gitkeep file
    with open(os.path.join(directory, ".gitkeep"), "w") as f:
        f.write("")

print("\n✓ Project setup complete!")
print("\nNext steps:")
print("1. cd {{ cookiecutter.project_slug }}")
print("2. cp .env.example .env")
print("3. Edit .env file with your settings")
print("4. poetry install")
print("5. cd frontend && npm install")
print("6. cd .. && task migrate")
print("7. task createsuperuser")
print("8. task dev")
print("\nHappy coding! 🚀")