from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.core.turnstile import TurnstileMixin
from .models import User


class LoginForm(TurnstileMixin, AuthenticationForm):
    """
    ログインフォーム
    """
    username = forms.EmailField(
        label=_("メールアドレス"),
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'メールアドレスを入力してください',
            'autocomplete': 'email',
        })
    )
    password = forms.CharField(
        label=_("パスワード"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'パスワードを入力してください',
            'autocomplete': 'current-password',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # usernameフィールドをemailフィールドとして扱う
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)


class SignupForm(TurnstileMixin, UserCreationForm):
    """
    ユーザー登録フォーム
    """
    email = forms.EmailField(
        label=_("メールアドレス"),
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'メールアドレスを入力してください',
            'autocomplete': 'email',
        })
    )
    username = forms.CharField(
        label=_("ユーザー名"),
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'ユーザー名を入力してください',
            'autocomplete': 'username',
        })
    )
    first_name = forms.CharField(
        label=_("名"),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '名を入力してください',
            'autocomplete': 'given-name',
        })
    )
    last_name = forms.CharField(
        label=_("姓"),
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '姓を入力してください',
            'autocomplete': 'family-name',
        })
    )
    password1 = forms.CharField(
        label=_("パスワード"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'パスワードを入力してください',
            'autocomplete': 'new-password',
        })
    )
    password2 = forms.CharField(
        label=_("パスワード（確認）"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'パスワードを再度入力してください',
            'autocomplete': 'new-password',
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("このメールアドレスは既に使用されています。"))
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomPasswordResetForm(TurnstileMixin, PasswordResetForm):
    """
    パスワードリセットフォーム
    """
    email = forms.EmailField(
        label=_("メールアドレス"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'メールアドレスを入力してください',
            'autocomplete': 'email',
        })
    )


class ProfileForm(forms.ModelForm):
    """
    プロフィール編集フォーム
    """
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'avatar', 'bio', 
            'phone_number', 'email_notifications'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '名を入力してください',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '姓を入力してください',
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100',
                'accept': 'image/*',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': '自己紹介を入力してください...',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '090-1234-5678',
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-300 focus:ring focus:ring-primary-200 focus:ring-opacity-50',
            }),
        }