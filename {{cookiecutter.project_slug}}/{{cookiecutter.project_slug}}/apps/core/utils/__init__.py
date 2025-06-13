"""
Core utilities package.
"""
from .email import send_template_email, send_admin_notification
from .pagination import paginate_queryset, get_page_range
from .files import (
    get_unique_filename,
    get_file_mime_type,
    validate_file_size,
    get_upload_to_path,
)

__all__ = [
    # Email utilities
    'send_template_email',
    'send_admin_notification',
    # Pagination utilities
    'paginate_queryset',
    'get_page_range',
    # File utilities
    'get_unique_filename',
    'get_file_mime_type',
    'validate_file_size',
    'get_upload_to_path',
]