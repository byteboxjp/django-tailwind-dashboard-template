"""
Email utility functions.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_template_email(
    subject,
    template_name,
    context,
    recipient_list,
    from_email=None,
    fail_silently=False
):
    """
    テンプレートを使用してメールを送信
    
    Args:
        subject: メールの件名
        template_name: メールテンプレートのパス
        context: テンプレートに渡すコンテキスト
        recipient_list: 受信者のリスト
        from_email: 送信元メールアドレス（省略時はDEFAULT_FROM_EMAILを使用）
        fail_silently: エラー時に例外を発生させないかどうか
    
    Returns:
        送信したメールの数
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    
    # HTMLメールの内容を生成
    html_message = render_to_string(template_name, context)
    
    # プレーンテキスト版を生成（HTMLタグを除去）
    plain_message = strip_tags(html_message)
    
    try:
        return send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=fail_silently,
        )
    except Exception as e:
        logger.error(f"メール送信エラー: {e}")
        if not fail_silently:
            raise
        return 0


def send_admin_notification(subject, message, html_message=None):
    """
    管理者にメール通知を送信
    
    Args:
        subject: メールの件名
        message: メール本文（プレーンテキスト）
        html_message: HTML形式のメール本文（オプション）
    
    Returns:
        送信したメールの数
    """
    admin_emails = [admin[1] for admin in settings.ADMINS]
    
    if not admin_emails:
        logger.warning("ADMINS設定が空のため、管理者通知を送信できません")
        return 0
    
    return send_mail(
        subject=f"[{settings.SITE_NAME}] {subject}",
        message=message,
        from_email=settings.SERVER_EMAIL,
        recipient_list=admin_emails,
        html_message=html_message,
        fail_silently=False,
    )