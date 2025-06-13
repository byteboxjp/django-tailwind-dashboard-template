from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.utils.translation import gettext_lazy as _

from .forms import LoginForm, SignupForm, CustomPasswordResetForm, ProfileForm
from .models import User


class LoginView(auth_views.LoginView):
    """
    ログインビュー
    """
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard:index')

    def form_valid(self, form):
        messages.success(self.request, _('ログインしました。'))
        return super().form_valid(form)


class LogoutView(auth_views.LogoutView):
    """
    ログアウトビュー
    """
    next_page = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _('ログアウトしました。'))
        return super().dispatch(request, *args, **kwargs)


class SignupView(CreateView):
    """
    ユーザー登録ビュー
    """
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('dashboard:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        # 登録後に自動ログイン
        auth_login(self.request, self.object)
        messages.success(self.request, _('アカウントが作成されました。'))
        return response

    def dispatch(self, request, *args, **kwargs):
        # 既にログイン済みの場合はダッシュボードにリダイレクト
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return super().dispatch(request, *args, **kwargs)


class PasswordResetView(auth_views.PasswordResetView):
    """
    パスワードリセットビュー
    """
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        messages.success(
            self.request,
            _('パスワードリセットメールを送信しました。メールをご確認ください。')
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    プロフィール表示ビュー
    """
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    プロフィール編集ビュー
    """
    model = User
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('プロフィールを更新しました。'))
        return super().form_valid(form)
