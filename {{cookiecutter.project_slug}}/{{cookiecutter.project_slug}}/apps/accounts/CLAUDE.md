# Accounts App - Claude Code ガイド

## 概要
ユーザー認証とアカウント管理を担当するアプリケーション。

## 主要コンポーネント

### Models (`models.py`)
- **User**: カスタムユーザーモデル
  - `email` を USERNAME_FIELD として使用
  - 追加フィールド: `avatar`, `bio`, `phone_number`, `email_notifications`

### Views (`views.py`)
- **LoginView**: メール/パスワードでログイン
- **SignupView**: 新規ユーザー登録
- **ProfileView**: プロファイル表示・編集
- **PasswordResetView**: パスワードリセット

### Forms (`forms.py`)
- **LoginForm**: {% if cookiecutter.use_cloudflare_turnstile == "y" %}Turnstile統合{% endif %}
- **SignupForm**: バリデーション付き登録フォーム
- **ProfileForm**: プロファイル編集

### URLs
- `/accounts/login/` - ログイン
- `/accounts/signup/` - 新規登録
- `/accounts/logout/` - ログアウト
- `/accounts/profile/` - プロファイル
- `/accounts/password-reset/` - パスワードリセット

## カスタマイズポイント
1. **認証方法の変更**: `LOGIN_URL`, `LOGIN_REDIRECT_URL`を設定で調整
2. **フィールド追加**: Userモデルを拡張してマイグレーション
3. **バリデーション**: forms.pyでカスタムバリデーション追加

## テスト
```bash
task test -- apps.accounts
```