"""
Test cases for accounts models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTestCase(TestCase):
    """Test cases for custom User model."""
    
    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': '太郎',
            'last_name': '山田',
        }
    
    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = User.objects.create_superuser(**self.user_data)
        
        self.assertEqual(superuser.username, self.user_data['username'])
        self.assertEqual(superuser.email, self.user_data['email'])
        self.assertTrue(superuser.check_password(self.user_data['password']))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
    
    def test_email_as_username_field(self):
        """Test that email is used as USERNAME_FIELD."""
        self.assertEqual(User.USERNAME_FIELD, 'email')
        self.assertIn('username', User.REQUIRED_FIELDS)
    
    def test_unique_email_constraint(self):
        """Test that email must be unique."""
        User.objects.create_user(**self.user_data)
        
        # Try to create another user with the same email
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'anotheruser'
        
        with self.assertRaises(Exception):
            User.objects.create_user(**duplicate_data)
    
    def test_str_representation(self):
        """Test string representation of User model."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), user.username)
    
    def test_get_full_name(self):
        """Test get_full_name method."""
        user = User.objects.create_user(**self.user_data)
        expected_name = f"{user.first_name} {user.last_name}"
        self.assertEqual(user.get_full_name(), expected_name)
    
    def test_profile_fields(self):
        """Test additional profile fields."""
        user = User.objects.create_user(**self.user_data)
        user.bio = "テストユーザーです。"
        user.phone_number = "090-1234-5678"
        user.email_notifications = False
        user.save()
        
        # Reload from database
        user.refresh_from_db()
        self.assertEqual(user.bio, "テストユーザーです。")
        self.assertEqual(user.phone_number, "090-1234-5678")
        self.assertFalse(user.email_notifications)