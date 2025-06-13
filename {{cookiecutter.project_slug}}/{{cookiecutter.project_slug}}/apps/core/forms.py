"""
Forms for core app.
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Contact
from .turnstile import TurnstileMixin


class ContactForm(TurnstileMixin, forms.ModelForm):
    """
    お問い合わせフォーム
    """
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('お名前を入力してください'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': _('メールアドレスを入力してください'),
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('件名を入力してください'),
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 5,
                'placeholder': _('お問い合わせ内容を入力してください'),
            }),
        }
        labels = {
            'name': _('お名前'),
            'email': _('メールアドレス'),
            'subject': _('件名'),
            'message': _('お問い合わせ内容'),
        }
        help_texts = {
            'email': _('ご返信先のメールアドレスを入力してください。'),
        }