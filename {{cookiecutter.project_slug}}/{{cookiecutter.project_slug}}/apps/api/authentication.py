"""
Custom authentication classes for API.
"""
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Session authentication without CSRF check for API endpoints.
    Use this only for trusted API endpoints.
    """
    
    def enforce_csrf(self, request):
        """
        Don't enforce CSRF for API endpoints.
        This is useful for mobile apps or external API clients.
        """
        return