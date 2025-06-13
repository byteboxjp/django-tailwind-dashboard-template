"""
Test cases for dashboard views.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class DashboardIndexViewTestCase(TestCase):
    """Test cases for dashboard index view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.dashboard_url = reverse('dashboard:index')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication."""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)
    
    def test_dashboard_renders_for_authenticated_user(self):
        """Test that dashboard renders for logged in user."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertContains(response, 'ダッシュボード')
    
    def test_dashboard_context_data(self):
        """Test dashboard context data."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.dashboard_url)
        
        # Check context variables
        self.assertIn('total_users', response.context)
        self.assertIn('new_users_today', response.context)
        self.assertIn('active_users', response.context)
        self.assertIn('total_revenue', response.context)
        self.assertIn('chart_data', response.context)
        
        # Verify chart data structure
        chart_data = response.context['chart_data']
        self.assertIsInstance(chart_data, str)
        
        # Parse JSON and verify structure
        chart_data_dict = json.loads(chart_data)
        self.assertIn('labels', chart_data_dict)
        self.assertIn('datasets', chart_data_dict)
        self.assertEqual(len(chart_data_dict['labels']), 7)  # 7 days
    
    def test_dashboard_statistics_calculation(self):
        """Test dashboard statistics calculation."""
        # Create additional users for testing
        for i in range(5):
            User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='password123'
            )
        
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.dashboard_url)
        
        # Check total users count
        self.assertEqual(response.context['total_users'], 6)  # Including test user
        
        # Check active users (all users are active by default)
        self.assertEqual(response.context['active_users'], 6)


class DashboardProfileViewTestCase(TestCase):
    """Test cases for dashboard profile view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.profile_url = reverse('dashboard:profile')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='太郎',
            last_name='山田'
        )
    
    def test_profile_view_renders(self):
        """Test that profile view renders correctly."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/profile.html')
        self.assertContains(response, 'プロフィール')
        self.assertContains(response, self.user.get_full_name())
    
    def test_profile_displays_user_info(self):
        """Test that profile displays correct user information."""
        self.user.bio = 'これはテストプロフィールです。'
        self.user.save()
        
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.profile_url)
        
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.bio)
        self.assertContains(response, self.user.username)


class DashboardSettingsViewTestCase(TestCase):
    """Test cases for dashboard settings view."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.settings_url = reverse('dashboard:settings')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_settings_view_renders(self):
        """Test that settings view renders correctly."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/settings.html')
        self.assertContains(response, '設定')
    
    def test_settings_sections(self):
        """Test that settings page shows all sections."""
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(self.settings_url)
        
        # Check for various settings sections
        self.assertContains(response, 'アカウント設定')
        self.assertContains(response, '通知設定')
        self.assertContains(response, 'セキュリティ')
        self.assertContains(response, 'プライバシー')


class DashboardAPITestCase(TestCase):
    """Test cases for dashboard API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_unauthenticated_api_access(self):
        """Test that API requires authentication."""
        # Test a hypothetical API endpoint
        response = self.client.get('/api/dashboard/stats/')
        self.assertIn(response.status_code, [302, 401, 403])  # Redirect or forbidden