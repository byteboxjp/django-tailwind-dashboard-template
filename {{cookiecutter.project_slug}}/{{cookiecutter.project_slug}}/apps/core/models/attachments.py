"""
File attachment models.
"""
import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from .base import TimeStampedModel, UUIDModel


def get_upload_path(instance, filename):
    """
    ファイルのアップロードパスを生成
    年/月/日/ファイル名の形式で保存
    """
    from django.utils import timezone
    now = timezone.now()
    return os.path.join(
        'attachments',
        str(now.year),
        str(now.month).zfill(2),
        str(now.day).zfill(2),
        filename
    )


class Attachment(TimeStampedModel, UUIDModel):
    """
    汎用ファイル添付モデル
    """
    ALLOWED_EXTENSIONS = [
        'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
        'txt', 'csv', 'zip', 'rar',
        'jpg', 'jpeg', 'png', 'gif', 'svg', 'webp',
        'mp4', 'avi', 'mov', 'wmv',
        'mp3', 'wav', 'ogg',
    ]
    
    file = models.FileField(
        _("ファイル"),
        upload_to=get_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)]
    )
    original_filename = models.CharField(
        _("オリジナルファイル名"),
        max_length=255
    )
    file_size = models.PositiveIntegerField(
        _("ファイルサイズ"),
        help_text=_("バイト単位")
    )
    mime_type = models.CharField(
        _("MIMEタイプ"),
        max_length=100,
        blank=True
    )
    description = models.TextField(
        _("説明"),
        blank=True
    )
    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_files',
        verbose_name=_("アップロードユーザー")
    )
    is_public = models.BooleanField(
        _("公開設定"),
        default=False,
        help_text=_("チェックすると誰でもアクセス可能になります")
    )
    download_count = models.PositiveIntegerField(
        _("ダウンロード数"),
        default=0
    )

    class Meta:
        verbose_name = _("添付ファイル")
        verbose_name_plural = _("添付ファイル")
        ordering = ['-created_at']

    def __str__(self):
        return self.original_filename

    def save(self, *args, **kwargs):
        """保存時にファイル情報を自動設定"""
        if self.file:
            self.original_filename = self.file.name
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    @property
    def file_size_display(self):
        """人間が読みやすいファイルサイズ表示"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def increment_download_count(self):
        """ダウンロード数をインクリメント"""
        self.download_count += 1
        self.save(update_fields=['download_count'])


class Image(TimeStampedModel, UUIDModel):
    """
    画像専用モデル（サムネイル生成機能付き）
    """
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']
    
    image = models.ImageField(
        _("画像"),
        upload_to=get_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)]
    )
    title = models.CharField(
        _("タイトル"),
        max_length=200,
        blank=True
    )
    alt_text = models.CharField(
        _("代替テキスト"),
        max_length=200,
        blank=True,
        help_text=_("アクセシビリティのための画像説明")
    )
    caption = models.TextField(
        _("キャプション"),
        blank=True
    )
    width = models.PositiveIntegerField(
        _("幅"),
        null=True,
        blank=True
    )
    height = models.PositiveIntegerField(
        _("高さ"),
        null=True,
        blank=True
    )
    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_images',
        verbose_name=_("アップロードユーザー")
    )

    class Meta:
        verbose_name = _("画像")
        verbose_name_plural = _("画像")
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Image {self.id}"

    def save(self, *args, **kwargs):
        """保存時に画像の幅と高さを取得"""
        if self.image and not self.width:
            from PIL import Image as PILImage
            with PILImage.open(self.image) as img:
                self.width, self.height = img.size
        super().save(*args, **kwargs)