"""
Test cases for core utilities.
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.core.utils import (
    generate_unique_filename, validate_file_size, 
    get_client_ip, slugify_ja
)


class UtilityFunctionsTestCase(TestCase):
    """Test cases for utility functions."""
    
    def test_generate_unique_filename(self):
        """Test unique filename generation."""
        # Test with regular filename
        filename = generate_unique_filename('test.jpg')
        self.assertTrue(filename.endswith('.jpg'))
        self.assertNotEqual(filename, 'test.jpg')
        self.assertEqual(len(filename.split('_')), 2)  # Should have UUID part
        
        # Test with filename containing spaces
        filename = generate_unique_filename('my file name.pdf')
        self.assertTrue(filename.endswith('.pdf'))
        self.assertNotIn(' ', filename)
        
        # Test with uppercase extension
        filename = generate_unique_filename('document.PDF')
        self.assertTrue(filename.endswith('.pdf'))
    
    def test_validate_file_size(self):
        """Test file size validation."""
        # Create a mock file under the limit
        small_file = SimpleUploadedFile(
            "test.txt",
            b"x" * 1000,  # 1KB
            content_type="text/plain"
        )
        
        # Should not raise exception for small file
        try:
            validate_file_size(small_file, max_size_mb=1)
        except Exception:
            self.fail("validate_file_size raised exception for small file")
        
        # Create a mock file over the limit
        large_file = SimpleUploadedFile(
            "test.txt",
            b"x" * (2 * 1024 * 1024),  # 2MB
            content_type="text/plain"
        )
        
        # Should raise exception for large file
        with self.assertRaises(Exception):
            validate_file_size(large_file, max_size_mb=1)
    
    def test_get_client_ip(self):
        """Test client IP extraction from request."""
        from django.test import RequestFactory
        
        factory = RequestFactory()
        
        # Test with direct client IP
        request = factory.get('/')
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        self.assertEqual(get_client_ip(request), '192.168.1.1')
        
        # Test with X-Forwarded-For header
        request = factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '10.0.0.1, 192.168.1.1'
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        self.assertEqual(get_client_ip(request), '10.0.0.1')
        
        # Test with X-Real-IP header
        request = factory.get('/')
        request.META['HTTP_X_REAL_IP'] = '172.16.0.1'
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        self.assertEqual(get_client_ip(request), '172.16.0.1')
    
    def test_slugify_ja(self):
        """Test Japanese text slugification."""
        # Test English text
        self.assertEqual(slugify_ja('Hello World'), 'hello-world')
        
        # Test Japanese text
        self.assertEqual(slugify_ja('こんにちは世界'), 'konnichiha-shi-jie')
        
        # Test mixed text
        self.assertEqual(slugify_ja('Django テスト'), 'django-tesuto')
        
        # Test with special characters
        self.assertEqual(slugify_ja('test@#$%'), 'test')
        
        # Test with numbers
        self.assertEqual(slugify_ja('テスト123'), 'tesuto123')