"""
Test cases for accounts forms.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.forms import LoginForm, SignupForm, ProfileForm, CustomPasswordResetForm

User = get_user_model()


class LoginFormTestCase(TestCase):
    """Test cases for LoginForm."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_valid_login_form(self):
        """Test login with valid credentials."""
        form_data = {
            'username': 'test@example.com',  # Email as username
            'password': 'testpass123'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_login_form(self):
        """Test login with invalid credentials."""
        form_data = {
            'username': 'test@example.com',
            'password': 'wrongpassword'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_empty_form(self):
        """Test empty login form."""
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)


class SignupFormTestCase(TestCase):
    """Test cases for SignupForm."""
    
    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': '花子',
            'last_name': '田中',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
    
    def test_valid_signup_form(self):
        """Test signup with valid data."""
        form = SignupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        
        # Save the form and check user creation
        user = form.save()
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.first_name, self.valid_data['first_name'])
        self.assertEqual(user.last_name, self.valid_data['last_name'])
    
    def test_password_mismatch(self):
        """Test signup with mismatched passwords."""
        data = self.valid_data.copy()
        data['password2'] = 'DifferentPass123!'
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_duplicate_email(self):
        """Test signup with existing email."""
        # Create a user with the same email
        User.objects.create_user(
            username='existinguser',
            email=self.valid_data['email'],
            password='password123'
        )
        
        form = SignupForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_weak_password(self):
        """Test signup with weak password."""
        data = self.valid_data.copy()
        data['password1'] = '123'
        data['password2'] = '123'
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())


class ProfileFormTestCase(TestCase):
    """Test cases for ProfileForm."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_valid_profile_update(self):
        """Test updating profile with valid data."""
        form_data = {
            'first_name': '太郎',
            'last_name': '山田',
            'bio': 'これはテストプロフィールです。',
            'phone_number': '090-1234-5678',
            'email_notifications': True
        }
        form = ProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        
        # Save and check updates
        user = form.save()
        self.assertEqual(user.first_name, form_data['first_name'])
        self.assertEqual(user.last_name, form_data['last_name'])
        self.assertEqual(user.bio, form_data['bio'])
        self.assertEqual(user.phone_number, form_data['phone_number'])
        self.assertTrue(user.email_notifications)
    
    def test_partial_update(self):
        """Test updating only some fields."""
        form_data = {
            'first_name': '次郎',
            'last_name': self.user.last_name,
            'email_notifications': False
        }
        form = ProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.first_name, '次郎')


class CustomPasswordResetFormTestCase(TestCase):
    """Test cases for CustomPasswordResetForm."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_valid_email(self):
        """Test password reset with valid email."""
        form = CustomPasswordResetForm(data={'email': 'test@example.com'})
        self.assertTrue(form.is_valid())
    
    def test_nonexistent_email(self):
        """Test password reset with non-existent email."""
        form = CustomPasswordResetForm(data={'email': 'nonexistent@example.com'})
        # Form should still be valid (for security reasons)
        self.assertTrue(form.is_valid())
    
    def test_invalid_email_format(self):
        """Test password reset with invalid email format."""
        form = CustomPasswordResetForm(data={'email': 'not-an-email'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)