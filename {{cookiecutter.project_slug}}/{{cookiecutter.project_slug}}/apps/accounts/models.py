from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    カスタムユーザーモデル
    """
    email = models.EmailField(_("email address"), unique=True)
    
    # プロフィール情報
    avatar = models.ImageField(
        _("avatar"),
        upload_to="avatars/",
        blank=True,
        null=True,
        help_text=_("User avatar image")
    )
    bio = models.TextField(
        _("bio"),
        max_length=500,
        blank=True,
        help_text=_("A short bio about the user")
    )
    
    # 追加フィールド
    phone_number = models.CharField(
        _("phone number"),
        max_length=17,
        blank=True,
        help_text=_("Phone number in international format")
    )
    
    # メタ情報
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    
    # 機能フラグ
    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_("Designates whether this user has verified their email address.")
    )
    
    # 通知設定
    email_notifications = models.BooleanField(
        _("email notifications"),
        default=True,
        help_text=_("Receive email notifications")
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username
    
    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name or self.username.split("@")[0]
