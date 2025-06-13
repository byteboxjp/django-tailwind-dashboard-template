"""
Test cases for Turnstile integration.
"""
from django.test import TestCase, override_settings
from django import forms
from unittest.mock import patch, Mock
from apps.core.turnstile import TurnstileWidget, TurnstileField, TurnstileMixin


class TurnstileWidgetTestCase(TestCase):
    """Test cases for TurnstileWidget."""
    
    def test_widget_initialization(self):
        """Test widget initialization with default values."""
        widget = TurnstileWidget()
        self.assertEqual(widget.theme, 'light')
        self.assertEqual(widget.size, 'normal')
    
    def test_widget_custom_attributes(self):
        """Test widget with custom attributes."""
        widget = TurnstileWidget(theme='dark', size='compact')
        self.assertEqual(widget.theme, 'dark')
        self.assertEqual(widget.size, 'compact')
    
    @override_settings(TURNSTILE_SITE_KEY='test-site-key')
    def test_widget_context(self):
        """Test widget context generation."""
        widget = TurnstileWidget()
        context = widget.get_context('turnstile', '', {})
        
        self.assertEqual(context['widget']['site_key'], 'test-site-key')
        self.assertEqual(context['widget']['theme'], 'light')
        self.assertEqual(context['widget']['size'], 'normal')


class TurnstileFieldTestCase(TestCase):
    """Test cases for TurnstileField."""
    
    @override_settings(TESTING=True)
    def test_field_in_test_mode(self):
        """Test that field skips validation in test mode."""
        field = TurnstileField()
        # Should not raise exception in test mode
        cleaned_value = field.clean('test-token')
        self.assertEqual(cleaned_value, 'test-token')
    
    def test_field_empty_value(self):
        """Test field validation with empty value."""
        field = TurnstileField()
        with self.assertRaises(forms.ValidationError):
            field.clean('')
    
    @override_settings(TURNSTILE_SECRET_KEY='')
    def test_field_no_secret_key(self):
        """Test field validation without secret key."""
        field = TurnstileField()
        with self.assertRaises(forms.ValidationError) as cm:
            field.clean('test-token')
        self.assertIn('Turnstile is not properly configured', str(cm.exception))
    
    @override_settings(TURNSTILE_SECRET_KEY='test-secret')
    @patch('requests.post')
    def test_field_successful_validation(self, mock_post):
        """Test field with successful validation."""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {'success': True}
        mock_post.return_value = mock_response
        
        field = TurnstileField()
        cleaned_value = field.clean('valid-token')
        self.assertEqual(cleaned_value, 'valid-token')
        
        # Verify API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn('secret', call_args[1]['data'])
        self.assertIn('response', call_args[1]['data'])
    
    @override_settings(TURNSTILE_SECRET_KEY='test-secret')
    @patch('requests.post')
    def test_field_failed_validation(self, mock_post):
        """Test field with failed validation."""
        # Mock failed response
        mock_response = Mock()
        mock_response.json.return_value = {
            'success': False,
            'error-codes': ['invalid-input-response']
        }
        mock_post.return_value = mock_response
        
        field = TurnstileField()
        with self.assertRaises(forms.ValidationError) as cm:
            field.clean('invalid-token')
        self.assertIn('Invalid CAPTCHA response', str(cm.exception))
    
    @override_settings(TURNSTILE_SECRET_KEY='test-secret')
    @patch('requests.post')
    def test_field_network_error(self, mock_post):
        """Test field with network error."""
        # Mock network error
        mock_post.side_effect = Exception('Network error')
        
        field = TurnstileField()
        with self.assertRaises(forms.ValidationError) as cm:
            field.clean('test-token')
        self.assertIn('Unable to verify CAPTCHA', str(cm.exception))


class TurnstileMixinTestCase(TestCase):
    """Test cases for TurnstileMixin."""
    
    class TestForm(TurnstileMixin, forms.Form):
        """Test form with TurnstileMixin."""
        name = forms.CharField()
    
    @override_settings(TURNSTILE_SITE_KEY='test-site-key')
    def test_mixin_adds_field(self):
        """Test that mixin adds turnstile field when configured."""
        form = self.TestForm()
        self.assertIn('turnstile', form.fields)
        self.assertIsInstance(form.fields['turnstile'], TurnstileField)
    
    @override_settings(TURNSTILE_SITE_KEY='')
    def test_mixin_no_field_without_key(self):
        """Test that mixin doesn't add field without site key."""
        form = self.TestForm()
        self.assertNotIn('turnstile', form.fields)
    
    def test_mixin_field_properties(self):
        """Test turnstile field properties."""
        with self.settings(TURNSTILE_SITE_KEY='test-site-key'):
            form = self.TestForm()
            field = form.fields['turnstile']
            self.assertEqual(field.label, '')
            self.assertEqual(field.help_text, 'Please verify you are human.')