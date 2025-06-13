"""
Core base models.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    タイムスタンプ付き抽象モデル
    """
    created_at = models.DateTimeField(
        _("作成日時"),
        auto_now_add=True,
        editable=False,
        db_index=True
    )
    updated_at = models.DateTimeField(
        _("更新日時"),
        auto_now=True,
        editable=False,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class UUIDModel(models.Model):
    """
    UUID主キーを持つ抽象モデル
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    論理削除機能を持つ抽象モデル
    """
    is_deleted = models.BooleanField(
        _("削除フラグ"),
        default=False,
        db_index=True
    )
    deleted_at = models.DateTimeField(
        _("削除日時"),
        null=True,
        blank=True,
        db_index=True
    )
    deleted_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_deleted',
        verbose_name=_("削除者")
    )

    class Meta:
        abstract = True

    def soft_delete(self, user=None):
        """論理削除を実行"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        self.save()

    def restore(self):
        """論理削除を取り消し"""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()


class PublishableModel(models.Model):
    """
    公開管理機能を持つ抽象モデル
    """
    is_published = models.BooleanField(
        _("公開状態"),
        default=False,
        db_index=True
    )
    published_at = models.DateTimeField(
        _("公開日時"),
        null=True,
        blank=True,
        db_index=True
    )
    published_until = models.DateTimeField(
        _("公開終了日時"),
        null=True,
        blank=True,
        db_index=True
    )

    class Meta:
        abstract = True

    @property
    def is_active(self):
        """現在公開中かどうかを判定"""
        if not self.is_published:
            return False
        
        now = timezone.now()
        
        if self.published_at and self.published_at > now:
            return False
        
        if self.published_until and self.published_until < now:
            return False
        
        return True


class OrderableModel(models.Model):
    """
    並び順管理機能を持つ抽象モデル
    """
    order = models.PositiveIntegerField(
        _("並び順"),
        default=0,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ['order', '-created_at']