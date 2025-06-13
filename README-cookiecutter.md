# Django Tailwind Dashboard Template

A production-ready Django project template with TailwindCSS, Alpine.js, and modern development tools.

## Features

- 🎨 **TailwindCSS** - Utility-first CSS framework with Flowbite components
- ⚡ **Alpine.js** - Lightweight reactive framework for UI interactions
- 🔐 **Custom User Model** - Email-based authentication ready
- 📊 **Dashboard** - Pre-built dashboard with charts and statistics
- 🏗️ **Modular Settings** - Separate settings for development/production
- 🛠️ **Development Tools** - Pre-commit hooks, Task automation, Poetry
- 🌐 **i18n Ready** - Japanese locale configured by default
- 🚀 **Production Ready** - Celery, Redis, PostgreSQL configurations

## Quick Start

```bash
# Install cookiecutter
pip install cookiecutter

# Generate project
cookiecutter https://github.com/yourusername/django-tailwind-dashboard-template

# Follow the prompts
project_name [My Django Project]: My Awesome App
project_slug [my_awesome_app]: 
author_name [Your Name]: John Doe
email [your.email@example.com]: john@example.com
# ... etc

# Navigate to project
cd my_awesome_app

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Install Python dependencies
poetry install

# Install frontend dependencies
cd frontend
npm install
cd ..

# Run migrations
task migrate

# Create superuser
task createsuperuser

# Start development server
task dev

# In another terminal, start CSS watcher
task css-watch
```

## Project Structure

```
my_awesome_app/
├── my_awesome_app/         # Django project directory
│   ├── apps/               # Django applications
│   │   ├── accounts/       # User authentication
│   │   ├── core/          # Core functionality
│   │   └── dashboard/     # Dashboard views
│   ├── config/            # Project configuration
│   │   └── settings/      # Modular settings
│   ├── static/            # Static files
│   └── templates/         # HTML templates
├── frontend/              # Frontend build tools
├── .env.example          # Environment variables template
├── pyproject.toml        # Poetry configuration
└── Taskfile.yml          # Task automation
```

## Available Tasks

Run `task --list` to see all available tasks:

- `task dev` - Start development server
- `task migrate` - Run database migrations
- `task test` - Run tests
- `task format` - Format code with black/isort
- `task lint` - Run linting checks
- `task css-build` - Build CSS files
- `task css-watch` - Watch and rebuild CSS

## Configuration Options

During project generation, you can configure:

- **Project name** - Human-readable project name
- **Project slug** - Python package name
- **Database engine** - PostgreSQL or SQLite
- **Use Celery** - Async task processing
- **Use Redis** - Caching and Celery broker
- **Use Sentry** - Error tracking
- **Use Cloudflare Turnstile** - CAPTCHA protection

## Development Workflow

1. **Pre-commit hooks** are automatically installed
2. **Code formatting** with Black and isort
3. **Linting** with Ruff and Flake8
4. **Security checks** with Bandit
5. **Secret detection** to prevent credential leaks

## Deployment

The template is production-ready with:

- Gunicorn configuration
- PostgreSQL support
- Redis caching
- Celery for async tasks
- Static file handling
- Environment-based settings

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.