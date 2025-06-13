"""
API v1 views.
"""
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.core.models import Contact, FAQ, Page
from apps.dashboard.models import Activity
from .serializers import (
    UserSerializer, UserProfileSerializer, ContactSerializer,
    FAQSerializer, PageSerializer, ActivitySerializer,
    DashboardStatsSerializer, PasswordChangeSerializer
)

User = get_user_model()


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Return the current user."""
        return self.request.user


class UserListView(generics.ListAPIView):
    """List users (admin only)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on permissions."""
        if self.request.user.is_staff:
            return super().get_queryset()
        # Regular users can only see active users
        return super().get_queryset().filter(is_active=True)


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet for Contact model."""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filter queryset based on permissions."""
        if self.request.user.is_staff:
            return super().get_queryset()
        # Regular users can only see their own contacts
        return super().get_queryset().filter(email=self.request.user.email)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def resolve(self, request, pk=None):
        """Mark contact as resolved."""
        contact = self.get_object()
        contact.status = 'resolved'
        contact.resolved_at = timezone.now()
        contact.save()
        return Response({'status': 'resolved'})


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for FAQ model (read-only)."""
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count on retrieve."""
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        return super().retrieve(request, *args, **kwargs)


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Page model (read-only)."""
    serializer_class = PageSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """Return only published pages."""
        return Page.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).select_related('author')


class ActivityListView(generics.ListAPIView):
    """List user activities."""
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return activities for the current user."""
        return Activity.objects.filter(
            user=self.request.user
        ).order_by('-created_at')[:50]


class DashboardStatsView(APIView):
    """Get dashboard statistics."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Return dashboard statistics."""
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        stats = {
            'total_users': User.objects.count(),
            'new_users_today': User.objects.filter(
                date_joined__gte=today_start
            ).count(),
            'active_users': User.objects.filter(
                last_login__gte=now - timedelta(days=30)
            ).count(),
            'total_contacts': Contact.objects.count(),
            'pending_contacts': Contact.objects.filter(
                status='pending'
            ).count(),
            'total_pages': Page.objects.filter(
                status='published'
            ).count(),
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)


class ChartDataView(APIView):
    """Get chart data for dashboard."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Return chart data for the last 7 days."""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=6)
        
        # Generate date labels
        dates = []
        current = start_date
        while current <= end_date:
            dates.append(current)
            current += timedelta(days=1)
        
        # Count users per day
        user_counts = []
        contact_counts = []
        
        for date in dates:
            user_count = User.objects.filter(
                date_joined__date=date
            ).count()
            contact_count = Contact.objects.filter(
                created_at__date=date
            ).count()
            
            user_counts.append(user_count)
            contact_counts.append(contact_count)
        
        data = {
            'labels': [date.strftime('%m/%d') for date in dates],
            'datasets': [
                {
                    'label': '新規ユーザー',
                    'data': user_counts,
                    'borderColor': 'rgb(59, 130, 246)',
                    'backgroundColor': 'rgba(59, 130, 246, 0.5)',
                },
                {
                    'label': 'お問い合わせ',
                    'data': contact_counts,
                    'borderColor': 'rgb(16, 185, 129)',
                    'backgroundColor': 'rgba(16, 185, 129, 0.5)',
                }
            ]
        }
        
        return Response(data)


class PasswordChangeView(APIView):
    """Change user password."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Change the user's password."""
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Log activity
            Activity.objects.create(
                user=user,
                action='password_changed',
                description='パスワードを変更しました',
                ip_address=self.get_client_ip(request)
            )
            
            return Response(
                {'detail': 'パスワードが変更されました。'},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        """Extract client IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip