#!/usr/bin/env python
"""Pre-generation cookiecutter hook."""
import re
import sys

PROJECT_SLUG = "{{ cookiecutter.project_slug }}"

if not re.match(r"^[a-z][a-z0-9_]*$", PROJECT_SLUG):
    print(f"ERROR: Project slug '{PROJECT_SLUG}' is not a valid Python identifier.")
    print("Project slug must start with a lowercase letter and contain only lowercase letters, numbers, and underscores.")
    sys.exit(1)

# Reserved Python keywords
PYTHON_KEYWORDS = [
    "and", "as", "assert", "async", "await", "break", "class", "continue", 
    "def", "del", "elif", "else", "except", "False", "finally", "for", 
    "from", "global", "if", "import", "in", "is", "lambda", "None", 
    "nonlocal", "not", "or", "pass", "raise", "return", "True", "try", 
    "while", "with", "yield"
]

if PROJECT_SLUG in PYTHON_KEYWORDS:
    print(f"ERROR: Project slug '{PROJECT_SLUG}' is a Python reserved keyword.")
    sys.exit(1)

# Django reserved names
DJANGO_RESERVED = ["admin", "settings", "urls", "wsgi", "asgi", "models", "views", "tests"]
if PROJECT_SLUG in DJANGO_RESERVED:
    print(f"WARNING: Project slug '{PROJECT_SLUG}' might conflict with Django internals.")
    
print(f"Creating project: {PROJECT_SLUG}")