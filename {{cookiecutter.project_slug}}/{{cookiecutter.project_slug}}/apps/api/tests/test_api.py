"""
Test cases for API endpoints.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.core.models import Contact, FAQ, Page

User = get_user_model()


class APITestCase(TestCase):
    """Base test case for API tests."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )


class UserAPITestCase(APITestCase):
    """Test cases for user API endpoints."""
    
    def test_get_user_profile(self):
        """Test getting user profile."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api_v1:user-profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)
    
    def test_update_user_profile(self):
        """Test updating user profile."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api_v1:user-profile')
        data = {
            'first_name': '太郎',
            'last_name': '山田',
            'bio': '更新されたプロフィール'
        }
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, '太郎')
        self.assertEqual(self.user.bio, '更新されたプロフィール')
    
    def test_change_password(self):
        """Test password change endpoint."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api_v1:password-change')
        data = {
            'old_password': 'testpass123',
            'new_password': 'NewPass123!',
            'confirm_password': 'NewPass123!'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass123!'))
    
    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints."""
        url = reverse('api_v1:user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ContactAPITestCase(APITestCase):
    """Test cases for contact API endpoints."""
    
    def test_create_contact(self):
        """Test creating a contact without authentication."""
        url = reverse('api_v1:contact-list')
        data = {
            'name': 'テストユーザー',
            'email': 'contact@example.com',
            'subject': 'テスト問い合わせ',
            'message': 'これはテストメッセージです。'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Contact.objects.filter(email='contact@example.com').exists())
    
    def test_list_contacts_as_staff(self):
        """Test listing contacts as staff user."""
        # Create some contacts
        Contact.objects.create(
            name='Contact 1',
            email='contact1@example.com',
            subject='Subject 1',
            message='Message 1'
        )
        
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('api_v1:contact-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
    
    def test_resolve_contact(self):
        """Test resolving a contact."""
        contact = Contact.objects.create(
            name='Test Contact',
            email='test@example.com',
            subject='Test',
            message='Test message'
        )
        
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('api_v1:contact-resolve', args=[contact.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contact.refresh_from_db()
        self.assertEqual(contact.status, 'resolved')
        self.assertIsNotNone(contact.resolved_at)


class FAQAPITestCase(APITestCase):
    """Test cases for FAQ API endpoints."""
    
    def test_list_faqs(self):
        """Test listing FAQs without authentication."""
        FAQ.objects.create(
            question='質問1',
            answer='回答1',
            category='general'
        )
        FAQ.objects.create(
            question='質問2',
            answer='回答2',
            category='technical',
            is_active=False
        )
        
        url = reverse('api_v1:faq-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only active FAQs should be returned
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_faq_increments_view_count(self):
        """Test that retrieving FAQ increments view count."""
        faq = FAQ.objects.create(
            question='Test Question',
            answer='Test Answer',
            view_count=0
        )
        
        url = reverse('api_v1:faq-detail', args=[faq.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        faq.refresh_from_db()
        self.assertEqual(faq.view_count, 1)


class DashboardAPITestCase(APITestCase):
    """Test cases for dashboard API endpoints."""
    
    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api_v1:dashboard-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_users', response.data)
        self.assertIn('new_users_today', response.data)
        self.assertIn('active_users', response.data)
        self.assertIn('total_contacts', response.data)
    
    def test_chart_data(self):
        """Test chart data endpoint."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api_v1:chart-data')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('labels', response.data)
        self.assertIn('datasets', response.data)
        self.assertEqual(len(response.data['labels']), 7)  # 7 days of data