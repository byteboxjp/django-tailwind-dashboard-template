"""
Static pages models.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .base import TimeStampedModel, PublishableModel, OrderableModel


class Page(TimeStampedModel, PublishableModel):
    """
    静的ページモデル（利用規約、プライバシーポリシー等）
    """
    SLUG_CHOICES = [
        ('terms', '利用規約'),
        ('privacy', 'プライバシーポリシー'),
        ('about', '会社概要'),
        ('help', 'ヘルプ'),
        ('contact', 'お問い合わせ'),
    ]
    
    slug = models.SlugField(
        _("スラッグ"),
        max_length=100,
        unique=True,
        choices=SLUG_CHOICES,
        help_text=_("URLに使用される識別子")
    )
    title = models.CharField(
        _("タイトル"),
        max_length=200
    )
    content = models.TextField(
        _("本文")
    )
    meta_description = models.TextField(
        _("メタディスクリプション"),
        max_length=160,
        blank=True,
        help_text=_("SEO用の説明文")
    )

    class Meta:
        verbose_name = _("ページ")
        verbose_name_plural = _("ページ")
        ordering = ['slug']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:page_detail', kwargs={'slug': self.slug})


class FAQ(TimeStampedModel, PublishableModel, OrderableModel):
    """
    よくある質問モデル
    """
    CATEGORY_CHOICES = [
        ('general', '一般'),
        ('account', 'アカウント'),
        ('billing', '料金'),
        ('technical', '技術的な質問'),
        ('other', 'その他'),
    ]
    
    category = models.CharField(
        _("カテゴリ"),
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general',
        db_index=True
    )
    question = models.TextField(
        _("質問")
    )
    answer = models.TextField(
        _("回答")
    )
    is_featured = models.BooleanField(
        _("注目の質問"),
        default=False,
        help_text=_("トップページに表示する")
    )

    class Meta:
        verbose_name = _("よくある質問")
        verbose_name_plural = _("よくある質問")
        ordering = ['category', 'order', '-created_at']

    def __str__(self):
        return self.question[:50]


class Contact(TimeStampedModel):
    """
    お問い合わせモデル
    """
    STATUS_CHOICES = [
        ('new', '新規'),
        ('in_progress', '対応中'),
        ('resolved', '解決済み'),
        ('closed', 'クローズ'),
    ]
    
    CATEGORY_CHOICES = [
        ('general', '一般的なお問い合わせ'),
        ('bug', '不具合報告'),
        ('feature', '機能要望'),
        ('billing', '料金について'),
        ('other', 'その他'),
    ]
    
    name = models.CharField(
        _("お名前"),
        max_length=100
    )
    email = models.EmailField(
        _("メールアドレス")
    )
    category = models.CharField(
        _("カテゴリ"),
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general'
    )
    subject = models.CharField(
        _("件名"),
        max_length=200
    )
    message = models.TextField(
        _("お問い合わせ内容")
    )
    status = models.CharField(
        _("ステータス"),
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        db_index=True
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contacts',
        verbose_name=_("ユーザー")
    )
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_contacts',
        verbose_name=_("担当者")
    )
    notes = models.TextField(
        _("管理者メモ"),
        blank=True
    )
    resolved_at = models.DateTimeField(
        _("解決日時"),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("お問い合わせ")
        verbose_name_plural = _("お問い合わせ")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.name}"