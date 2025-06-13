"""
API v1 serializers.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.core.models import Contact, FAQ, Page
from apps.dashboard.models import Activity

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'bio', 'avatar', 'date_joined', 'is_active'
        ]
        read_only_fields = ['id', 'date_joined', 'is_active']


class UserProfileSerializer(serializers.ModelSerializer):
    """Detailed serializer for user profile."""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'bio', 'avatar', 'phone_number', 
            'email_notifications', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'username', 'email', 'date_joined', 'last_login']


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""
    
    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'email', 'subject', 'message',
            'status', 'created_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'created_at', 'resolved_at']
    
    def create(self, validated_data):
        """Create a new contact inquiry."""
        # Add IP address if available
        request = self.context.get('request')
        if request:
            validated_data['ip_address'] = self.get_client_ip(request)
        return super().create(validated_data)
    
    def get_client_ip(self, request):
        """Extract client IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class FAQSerializer(serializers.ModelSerializer):
    """Serializer for FAQ model."""
    
    class Meta:
        model = FAQ
        fields = [
            'id', 'question', 'answer', 'category',
            'order', 'is_active', 'view_count'
        ]
        read_only_fields = ['id', 'view_count']


class PageSerializer(serializers.ModelSerializer):
    """Serializer for Page model."""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = Page
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'author', 'author_name', 'status', 'published_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model."""
    user_display = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'user_display', 'action',
            'description', 'ip_address', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    total_users = serializers.IntegerField()
    new_users_today = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_contacts = serializers.IntegerField()
    pending_contacts = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    
    
class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        """Validate password change data."""
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'パスワードが一致しません。'
            })
        return data
    
    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('現在のパスワードが正しくありません。')
        return value