"""
Cloudflare Turnstile integration for Django forms.
"""
import os
import requests
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TurnstileWidget(forms.Widget):
    """Custom widget for Cloudflare Turnstile."""
    
    template_name = 'core/widgets/turnstile.html'
    
    def __init__(self, attrs=None, theme='light', size='normal'):
        self.theme = theme
        self.size = size
        super().__init__(attrs)
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'site_key': getattr(settings, 'TURNSTILE_SITE_KEY', ''),
            'theme': self.theme,
            'size': self.size,
        })
        return context


class TurnstileField(forms.CharField):
    """Form field for Cloudflare Turnstile validation."""
    
    widget = TurnstileWidget
    
    def __init__(self, *args, **kwargs):
        self.verify_url = kwargs.pop('verify_url', None) or getattr(
            settings, 
            'TURNSTILE_VERIFY_URL', 
            'https://challenges.cloudflare.com/turnstile/v0/siteverify'
        )
        super().__init__(*args, **kwargs)
        self.required = True
        self.error_messages['required'] = _('Please complete the CAPTCHA.')
    
    def clean(self, value):
        """Validate the Turnstile token."""
        if not value:
            raise ValidationError(self.error_messages['required'])
        
        # Skip validation in test mode
        if getattr(settings, 'TESTING', False):
            return value
        
        # Get secret key
        secret_key = getattr(settings, 'TURNSTILE_SECRET_KEY', '')
        if not secret_key:
            raise ValidationError(_('Turnstile is not properly configured.'))
        
        # Verify with Cloudflare
        try:
            response = requests.post(
                self.verify_url,
                data={
                    'secret': secret_key,
                    'response': value,
                },
                timeout=5
            )
            result = response.json()
            
            if not result.get('success', False):
                error_codes = result.get('error-codes', [])
                if 'missing-input-secret' in error_codes:
                    raise ValidationError(_('Turnstile configuration error.'))
                elif 'invalid-input-response' in error_codes:
                    raise ValidationError(_('Invalid CAPTCHA response.'))
                elif 'timeout-or-duplicate' in error_codes:
                    raise ValidationError(_('CAPTCHA timeout or duplicate.'))
                else:
                    raise ValidationError(_('CAPTCHA verification failed.'))
                    
        except requests.RequestException:
            raise ValidationError(_('Unable to verify CAPTCHA. Please try again.'))
        
        return value


class TurnstileMixin:
    """Mixin to add Turnstile field to forms."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if getattr(settings, 'TURNSTILE_SITE_KEY', None):
            self.fields['turnstile'] = TurnstileField(
                label='',
                help_text=_('Please verify you are human.')
            )