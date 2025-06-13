"""
Core app admin configuration.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Page, FAQ, Contact, Attachment, Image


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'published_at', 'created_at']
    list_filter = ['is_published', 'slug', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ['title']} if 'slug' not in [choice[0] for choice in Page.SLUG_CHOICES] else {}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('slug', 'title', 'content')
        }),
        (_('公開設定'), {
            'fields': ('is_published', 'published_at', 'published_until')
        }),
        (_('SEO'), {
            'fields': ('meta_description',)
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_featured', 'is_published', 'created_at']
    list_filter = ['category', 'is_featured', 'is_published', 'created_at']
    list_editable = ['order', 'is_featured', 'is_published']
    search_fields = ['question', 'answer']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('category', 'question', 'answer')
        }),
        (_('表示設定'), {
            'fields': ('order', 'is_featured', 'is_published', 'published_at', 'published_until')
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('お問い合わせ情報'), {
            'fields': ('name', 'email', 'category', 'subject', 'message')
        }),
        (_('対応状況'), {
            'fields': ('status', 'assigned_to', 'notes', 'resolved_at')
        }),
        (_('関連情報'), {
            'fields': ('user', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'assigned_to')


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'file_size_display', 'mime_type', 'uploaded_by', 'is_public', 'created_at']
    list_filter = ['is_public', 'mime_type', 'created_at']
    search_fields = ['original_filename', 'description']
    readonly_fields = ['id', 'file_size', 'file_size_display', 'download_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('file', 'description')
        }),
        (_('ファイル情報'), {
            'fields': ('id', 'original_filename', 'file_size', 'file_size_display', 'mime_type')
        }),
        (_('アクセス設定'), {
            'fields': ('is_public', 'download_count')
        }),
        (_('メタ情報'), {
            'fields': ('uploaded_by', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('uploaded_by')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'width', 'height', 'uploaded_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'alt_text', 'caption']
    readonly_fields = ['id', 'width', 'height', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('image', 'title', 'alt_text', 'caption')
        }),
        (_('画像情報'), {
            'fields': ('id', 'width', 'height')
        }),
        (_('メタ情報'), {
            'fields': ('uploaded_by', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('uploaded_by')
