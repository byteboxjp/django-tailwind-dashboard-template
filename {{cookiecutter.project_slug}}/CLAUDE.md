# Claude Code プロジェクトガイド

このドキュメントは、Claude Codeがプロジェクトの構造と要件を素早く理解するためのガイドです。

## 🎯 プロジェクト概要

**プロジェクト名**: {{ cookiecutter.project_name }}
**説明**: {{ cookiecutter.project_description }}
**バージョン**: {{ cookiecutter.project_version }}
**作成者**: {{ cookiecutter.author_name }} <{{ cookiecutter.email }}>

### 技術スタック
- **Backend**: Django {{ cookiecutter.django_version }}
- **Frontend**: TailwindCSS + Alpine.js
- **Database**: {% if cookiecutter.database_engine == "postgresql" %}PostgreSQL {{ cookiecutter.postgresql_version }}{% else %}SQLite3{% endif %}
- **Task Runner**: Taskfile
- **Package Manager**: Poetry (Python) / NPM (Frontend)
{% if cookiecutter.use_celery == "y" %}- **Async Tasks**: Celery + Redis{% endif %}
{% if cookiecutter.use_cloudflare_turnstile == "y" %}- **CAPTCHA**: Cloudflare Turnstile{% endif %}

## 📁 プロジェクト構造

```
{{ cookiecutter.project_slug }}/
├── {{ cookiecutter.project_slug }}/         # Djangoプロジェクトルート
│   ├── apps/                                # アプリケーションディレクトリ
│   │   ├── accounts/                        # 認証・ユーザー管理
│   │   ├── core/                           # 共通機能・ユーティリティ
│   │   ├── dashboard/                      # ダッシュボード機能
│   │   └── api/                            # REST API (DRF)
│   ├── config/                             # 設定ファイル
│   │   ├── settings/                       # 環境別設定
│   │   │   ├── base.py                    # 基本設定
│   │   │   ├── local.py                   # 開発環境
│   │   │   ├── production.py              # 本番環境
│   │   │   └── test.py                    # テスト環境
│   │   ├── urls.py                         # URLルーティング
│   │   └── wsgi.py                         # WSGI設定
│   ├── static/                             # 静的ファイル
│   │   ├── css/                            # スタイルシート
│   │   ├── js/                             # JavaScript
│   │   └── images/                         # 画像ファイル
│   └── templates/                          # HTMLテンプレート
├── frontend/                               # フロントエンドビルド設定
│   ├── package.json                        # NPM依存関係
│   └── tailwind.config.js                  # TailwindCSS設定
├── docs/                                   # ドキュメント
├── scripts/                                # デプロイ・ユーティリティスクリプト
├── tests/                                  # プロジェクトレベルのテスト
├── .env.example                           # 環境変数サンプル
├── pyproject.toml                         # Poetry設定・依存関係
└── Taskfile.yml                           # タスクランナー設定
```

## 🔑 重要な設定・カスタマイズポイント

### 1. カスタムユーザーモデル
- **場所**: `apps/accounts/models.py`
- **特徴**: メールアドレスをUSERNAME_FIELDとして使用
- **拡張フィールド**: avatar, bio, phone_number, email_notifications

### 2. 認証フロー
- **ログイン**: メールアドレス + パスワード
- **新規登録**: メール、ユーザー名、パスワード必須
- **パスワードリセット**: メールベース
{% if cookiecutter.use_cloudflare_turnstile == "y" %}- **CAPTCHA**: 全認証フォームにTurnstile統合{% endif %}

### 3. 再利用可能なモデル (apps/core/models/)
- `TimeStampedModel`: created_at, updated_at自動管理
- `UUIDModel`: UUID主キー
- `SoftDeleteModel`: 論理削除機能
- `PublishableModel`: 公開管理（draft/published/scheduled）
- `OrderableModel`: 順序管理

### 4. API構造 (apps/api/)
- **バージョニング**: /api/v1/
- **認証**: SessionAuthentication (CSRF exempt可)
- **主要エンドポイント**:
  - `/api/v1/users/profile/` - ユーザープロファイル
  - `/api/v1/dashboard/stats/` - ダッシュボード統計
  - `/api/v1/contacts/` - お問い合わせ管理

### 5. フロントエンド統合
- **Alpine.js Store** (`static/js/main.js`):
  - `darkMode` - ダークモード管理
  - `sidebar` - サイドバー開閉
  - `notifications` - 通知表示
- **APIクライアント** (`static/js/api.js`): 
  - REST APIとの通信ユーティリティ

## 🚀 開発コマンド

### 基本的なコマンド
```bash
# 開発サーバー起動
task dev

# データベースマイグレーション
task migrate

# スーパーユーザー作成
task createsuperuser

# テスト実行
task test

# Djangoシェル
task shell

# コードフォーマット
task format

# リンティング
task lint
```

### フロントエンド
```bash
# CSS監視・ビルド
task css-watch

# CSS本番ビルド
task css-build

# NPMパッケージインストール
task npm-install
```

### データベース操作
```bash
# ローカルDB作成 (PostgreSQL)
task create_local_database

# DBリセット
task reset_local_database

# DBダンプ
task dump_local_database

# DBリストア
task load_local_database
```

## 🔧 環境変数 (.env)

### 必須設定
- `SECRET_KEY` - Django秘密鍵（必ず変更）
- `ALLOWED_HOSTS` - 許可するホスト名
- `DATABASE_URL` または個別のDB設定

### オプション設定
{% if cookiecutter.use_celery == "y" %}- `CELERY_BROKER_URL` - Celeryブローカー設定
- `REDIS_HOST`, `REDIS_PORT` - Redis接続情報{% endif %}
{% if cookiecutter.use_cloudflare_turnstile == "y" %}- `TURNSTILE_SITE_KEY` - Cloudflare Turnstileサイトキー
- `TURNSTILE_SECRET_KEY` - Cloudflare Turnstile秘密鍵{% endif %}
{% if cookiecutter.use_sentry == "y" %}- `SENTRY_DSN` - Sentryエラートラッキング{% endif %}

## 📝 コーディング規約

### Python
- **フォーマッター**: Black (line-length: 120)
- **インポート整理**: isort (profile: black)
- **リンター**: Ruff + Flake8
- **型チェック**: Pyright
- **セキュリティ**: Bandit

### JavaScript/CSS
- **フォーマッター**: Prettier
- **設定**: .prettierrc (プロジェクトルート)

### Git
- **pre-commit hooks**: 自動フォーマット・リンティング
- **コミットメッセージ**: Conventional Commits推奨

## 🧪 テスト

### テスト構造
```
apps/
├── accounts/tests/
│   ├── test_models.py    # ユーザーモデルのテスト
│   ├── test_forms.py     # 認証フォームのテスト
│   └── test_views.py     # 認証ビューのテスト
├── core/tests/
│   ├── test_models.py    # 基本モデルのテスト
│   ├── test_utils.py     # ユーティリティのテスト
│   └── test_turnstile.py # Turnstileのテスト
└── api/tests/
    └── test_api.py       # APIエンドポイントのテスト
```

### テスト実行
```bash
# 全テスト実行
task test

# 特定アプリのテスト
task test -- apps.accounts

# カバレッジ付き
poetry run pytest --cov=apps --cov-report=html
```

## 🚨 注意事項・既知の問題

1. **カスタムユーザーモデル**: マイグレーション前に`AUTH_USER_MODEL`が正しく設定されていることを確認
2. **メール認証**: `email`フィールドがユニークかつ必須
3. **タイムゾーン**: デフォルトは`{{ cookiecutter.timezone }}`に設定
4. **静的ファイル**: 本番環境では`collectstatic`が必要
{% if cookiecutter.use_celery == "y" %}5. **Celery**: Redisが起動していることを確認{% endif %}

## 🔗 関連ドキュメント

- [デプロイガイド](docs/deployment.md)
- [API仕様書](apps/api/README.md)
- [Django公式ドキュメント](https://docs.djangoproject.com/)
- [TailwindCSS](https://tailwindcss.com/docs)
- [Alpine.js](https://alpinejs.dev/)

## 💡 Claude Codeへのヒント

### よくある作業パターン
1. **新しいアプリ追加**: `task startapp -- アプリ名`
2. **モデル追加後**: `task migrate`を実行
3. **静的ファイル変更後**: ブラウザのキャッシュクリア推奨
4. **テンプレート変更**: Django開発サーバーは自動リロード

### デバッグ方法
- **Django Debug Toolbar**: 開発環境で自動有効
- **ログ確認**: `logs/`ディレクトリ
- **Djangoシェル**: `task shell`でインタラクティブデバッグ

### パフォーマンス最適化
- **クエリ最適化**: `select_related()`, `prefetch_related()`の使用
- **キャッシュ**: Redis経由でのキャッシュ設定済み
- **静的ファイル**: 本番環境ではWhiteNoiseまたはCDN推奨

---

最終更新: {% now 'local' %}