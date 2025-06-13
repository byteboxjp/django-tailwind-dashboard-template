"""
Test cases for accounts views.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()


class LoginViewTestCase(TestCase):
    """Test cases for login view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_page_renders(self):
        """Test that login page renders correctly."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'ログイン')
    
    def test_successful_login(self):
        """Test successful login."""
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard:index'))
        
        # Check if user is logged in
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
    
    def test_failed_login(self):
        """Test failed login with wrong password."""
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'メールアドレスまたはパスワードが正しくありません')
    
    def test_redirect_authenticated_user(self):
        """Test that authenticated users are redirected."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard:index'))


class SignupViewTestCase(TestCase):
    """Test cases for signup view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.signup_url = reverse('accounts:signup')
    
    def test_signup_page_renders(self):
        """Test that signup page renders correctly."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertContains(response, 'アカウント作成')
    
    def test_successful_signup(self):
        """Test successful user registration."""
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': '花子',
            'last_name': '田中',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))
        
        # Check if user was created
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('アカウントが作成されました' in str(m) for m in messages))
    
    def test_signup_with_existing_email(self):
        """Test signup with already registered email."""
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='password123'
        )
        
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'このメールアドレスは既に使用されています')


class ProfileViewTestCase(TestCase):
    """Test cases for profile view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.profile_url = reverse('accounts:profile')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_requires_login(self):
        """Test that profile page requires authentication."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)
    
    def test_profile_page_renders(self):
        """Test that profile page renders for authenticated user."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, 'プロフィール')
    
    def test_profile_update(self):
        """Test updating user profile."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.post(self.profile_url, {
            'first_name': '太郎',
            'last_name': '山田',
            'bio': '更新されたプロフィール',
            'phone_number': '090-9876-5432',
            'email_notifications': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)
        
        # Check if profile was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, '太郎')
        self.assertEqual(self.user.last_name, '山田')
        self.assertEqual(self.user.bio, '更新されたプロフィール')
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('プロフィールが更新されました' in str(m) for m in messages))


class LogoutViewTestCase(TestCase):
    """Test cases for logout view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.logout_url = reverse('accounts:logout')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_logout(self):
        """Test user logout."""
        # Login first
        self.client.login(username='test@example.com', password='testpass123')
        
        # Logout
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))
        
        # Check if user is logged out
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 302)  # Redirected to login