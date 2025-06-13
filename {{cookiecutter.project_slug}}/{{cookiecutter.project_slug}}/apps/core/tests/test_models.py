"""
Test cases for core models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.core.models import (
    TimeStampedModel, UUIDModel, SoftDeleteModel, 
    PublishableModel, OrderableModel, Page, 
    Contact, FAQ, Attachment
)

User = get_user_model()


class MockTimeStampedModel(TimeStampedModel):
    """Mock model for testing TimeStampedModel."""
    class Meta:
        app_label = 'core'


class MockSoftDeleteModel(SoftDeleteModel):
    """Mock model for testing SoftDeleteModel."""
    class Meta:
        app_label = 'core'


class MockPublishableModel(PublishableModel):
    """Mock model for testing PublishableModel."""
    class Meta:
        app_label = 'core'


class AbstractModelTestCase(TestCase):
    """Test cases for abstract base models."""
    
    def test_timestamped_model(self):
        """Test TimeStampedModel functionality."""
        obj = MockTimeStampedModel()
        obj.save()
        
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)
        self.assertEqual(obj.created_at, obj.updated_at)
        
        # Update the object
        initial_updated = obj.updated_at
        obj.save()
        obj.refresh_from_db()
        
        self.assertNotEqual(initial_updated, obj.updated_at)
        self.assertEqual(obj.created_at.date(), initial_updated.date())
    
    def test_soft_delete_model(self):
        """Test SoftDeleteModel functionality."""
        obj = MockSoftDeleteModel()
        obj.save()
        
        # Object should not be deleted initially
        self.assertIsNone(obj.deleted_at)
        self.assertFalse(obj.is_deleted)
        
        # Soft delete the object
        obj.delete()
        obj.refresh_from_db()
        
        self.assertIsNotNone(obj.deleted_at)
        self.assertTrue(obj.is_deleted)
        
        # Restore the object
        obj.restore()
        obj.refresh_from_db()
        
        self.assertIsNone(obj.deleted_at)
        self.assertFalse(obj.is_deleted)
    
    def test_publishable_model(self):
        """Test PublishableModel functionality."""
        now = timezone.now()
        
        # Test draft status
        draft = MockPublishableModel(status='draft')
        draft.save()
        self.assertFalse(draft.is_published)
        
        # Test published status
        published = MockPublishableModel(
            status='published',
            published_at=now - timedelta(hours=1)
        )
        published.save()
        self.assertTrue(published.is_published)
        
        # Test scheduled status (future publish)
        scheduled = MockPublishableModel(
            status='scheduled',
            published_at=now + timedelta(hours=1)
        )
        scheduled.save()
        self.assertFalse(scheduled.is_published)
        
        # Test scheduled status (past publish)
        past_scheduled = MockPublishableModel(
            status='scheduled',
            published_at=now - timedelta(hours=1)
        )
        past_scheduled.save()
        self.assertTrue(past_scheduled.is_published)


class PageModelTestCase(TestCase):
    """Test cases for Page model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_page(self):
        """Test creating a page."""
        page = Page.objects.create(
            title='利用規約',
            slug='terms',
            content='これは利用規約のテストページです。',
            author=self.user,
            status='published'
        )
        
        self.assertEqual(page.title, '利用規約')
        self.assertEqual(page.slug, 'terms')
        self.assertEqual(page.author, self.user)
        self.assertEqual(str(page), '利用規約')
    
    def test_page_ordering(self):
        """Test page ordering."""
        page1 = Page.objects.create(
            title='ページ1',
            slug='page1',
            author=self.user,
            status='published'
        )
        page2 = Page.objects.create(
            title='ページ2',
            slug='page2',
            author=self.user,
            status='published'
        )
        
        pages = Page.objects.all()
        # Should be ordered by created_at descending
        self.assertEqual(pages[0], page2)
        self.assertEqual(pages[1], page1)


class ContactModelTestCase(TestCase):
    """Test cases for Contact model."""
    
    def test_create_contact(self):
        """Test creating a contact inquiry."""
        contact = Contact.objects.create(
            name='山田太郎',
            email='yamada@example.com',
            subject='お問い合わせテスト',
            message='これはテストメッセージです。'
        )
        
        self.assertEqual(contact.name, '山田太郎')
        self.assertEqual(contact.email, 'yamada@example.com')
        self.assertEqual(contact.status, 'pending')
        self.assertFalse(contact.is_resolved)
        self.assertEqual(str(contact), 'お問い合わせテスト - yamada@example.com')
    
    def test_resolve_contact(self):
        """Test resolving a contact inquiry."""
        contact = Contact.objects.create(
            name='テストユーザー',
            email='test@example.com',
            subject='テスト',
            message='テストメッセージ'
        )
        
        # Resolve the contact
        contact.status = 'resolved'
        contact.resolved_at = timezone.now()
        contact.save()
        
        self.assertTrue(contact.is_resolved)
        self.assertIsNotNone(contact.resolved_at)


class FAQModelTestCase(TestCase):
    """Test cases for FAQ model."""
    
    def test_create_faq(self):
        """Test creating an FAQ."""
        faq = FAQ.objects.create(
            question='これはどのように動作しますか？',
            answer='これは次のように動作します...',
            category='general',
            order=1
        )
        
        self.assertEqual(faq.question, 'これはどのように動作しますか？')
        self.assertEqual(faq.category, 'general')
        self.assertTrue(faq.is_active)
        self.assertEqual(str(faq), 'これはどのように動作しますか？')
    
    def test_faq_ordering(self):
        """Test FAQ ordering."""
        faq1 = FAQ.objects.create(
            question='質問1',
            answer='回答1',
            order=2
        )
        faq2 = FAQ.objects.create(
            question='質問2',
            answer='回答2',
            order=1
        )
        
        faqs = FAQ.objects.all()
        # Should be ordered by order field
        self.assertEqual(faqs[0], faq2)
        self.assertEqual(faqs[1], faq1)