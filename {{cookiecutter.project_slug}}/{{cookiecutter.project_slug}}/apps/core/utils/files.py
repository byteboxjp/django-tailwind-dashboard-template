"""
File handling utility functions.
"""
import os
import hashlib
from django.utils.text import slugify
from django.utils import timezone
import magic


def get_unique_filename(filename):
    """
    ユニークなファイル名を生成
    
    Args:
        filename: 元のファイル名
    
    Returns:
        ユニークなファイル名
    """
    name, ext = os.path.splitext(filename)
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    unique_id = hashlib.md5(f"{name}{timestamp}".encode()).hexdigest()[:8]
    safe_name = slugify(name)
    
    return f"{safe_name}_{unique_id}{ext}"


def get_file_mime_type(file_path):
    """
    ファイルのMIMEタイプを取得
    
    Args:
        file_path: ファイルパス
    
    Returns:
        MIMEタイプ文字列
    """
    try:
        mime = magic.Magic(mime=True)
        return mime.from_file(file_path)
    except Exception:
        # python-magicが利用できない場合は拡張子から推測
        ext = os.path.splitext(file_path)[1].lower()
        mime_types = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.zip': 'application/zip',
        }
        return mime_types.get(ext, 'application/octet-stream')


def validate_file_size(file, max_size_mb=10):
    """
    ファイルサイズをバリデーション
    
    Args:
        file: アップロードされたファイル
        max_size_mb: 最大ファイルサイズ（MB）
    
    Returns:
        bool: バリデーション結果
    
    Raises:
        ValueError: ファイルサイズが制限を超えている場合
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file.size > max_size_bytes:
        raise ValueError(
            f"ファイルサイズが制限を超えています。"
            f"最大{max_size_mb}MBまでアップロード可能です。"
        )
    
    return True


def get_upload_to_path(instance, filename, base_dir='uploads'):
    """
    モデルインスタンスに基づいてアップロードパスを生成
    
    Args:
        instance: モデルインスタンス
        filename: ファイル名
        base_dir: ベースディレクトリ
    
    Returns:
        アップロードパス
    """
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name
    date_path = timezone.now().strftime('%Y/%m/%d')
    unique_filename = get_unique_filename(filename)
    
    return os.path.join(
        base_dir,
        app_label,
        model_name,
        date_path,
        unique_filename
    )