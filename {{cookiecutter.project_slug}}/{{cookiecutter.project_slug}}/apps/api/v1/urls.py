"""
API v1 URL configuration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileView, UserListView, ContactViewSet,
    FAQViewSet, PageViewSet, ActivityListView,
    DashboardStatsView, ChartDataView, PasswordChangeView
)

app_name = 'api_v1'

# Create router and register viewsets
router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'faqs', FAQViewSet, basename='faq')
router.register(r'pages', PageViewSet, basename='page')

urlpatterns = [
    # User endpoints
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/password/', PasswordChangeView.as_view(), name='password-change'),
    
    # Activity endpoints
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    
    # Dashboard endpoints
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('dashboard/charts/', ChartDataView.as_view(), name='chart-data'),
    
    # Include router URLs
    path('', include(router.urls)),
]