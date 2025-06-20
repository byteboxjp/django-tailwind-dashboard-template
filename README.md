# Django Tailwind Dashboard Template

[English](#english) | [日本語](#japanese)

---

<a name="english"></a>
## 🌟 English

A production-ready Django project template with TailwindCSS, Alpine.js, and modern development tools.

### Features

- 🎨 **TailwindCSS** - Utility-first CSS framework with Flowbite components
- ⚡ **Alpine.js** - Lightweight reactive framework for UI interactions
- 🔐 **Custom User Model** - Email-based authentication ready
- 📊 **Dashboard** - Pre-built dashboard with charts and statistics
- 🏗️ **Modular Settings** - Separate settings for development/production
- 🛠️ **Development Tools** - Pre-commit hooks, Task automation, Poetry
- 🌐 **i18n Ready** - Japanese locale configured by default
- 🚀 **Production Ready** - Celery, Redis, PostgreSQL configurations

### Quick Start

```bash
# Install cookiecutter
pip install cookiecutter

# Generate project
cookiecutter https://github.com/byteboxjp/django-tailwind-dashboard-template

# Follow the prompts
project_name [My Django Project]: My Awesome App
project_slug [my_awesome_app]:
author_name [Your Name]: John Doe
email [your.email@example.com]: john@example.com
# ... etc

# Navigate to project
cd my_awesome_app

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Install Python dependencies
poetry install

# Install frontend dependencies
cd frontend
npm install
cd ..

# Run migrations
task migrate

# Create superuser
task createsuperuser

# Start development server
task dev

# In another terminal, start CSS watcher
task css-watch
```

### Project Structure

```
my_awesome_app/
├── my_awesome_app/         # Django project directory
│   ├── apps/               # Django applications
│   │   ├── accounts/       # User authentication
│   │   ├── core/          # Core functionality
│   │   └── dashboard/     # Dashboard views
│   ├── config/            # Project configuration
│   │   └── settings/      # Modular settings
│   ├── static/            # Static files
│   └── templates/         # HTML templates
├── frontend/              # Frontend build tools
├── .env.example          # Environment variables template
├── pyproject.toml        # Poetry configuration
└── Taskfile.yml          # Task automation
```

### Available Tasks

Run `task --list` to see all available tasks:

- `task dev` - Start development server
- `task migrate` - Run database migrations
- `task test` - Run tests
- `task format` - Format code with black/isort
- `task lint` - Run linting checks
- `task css-build` - Build CSS files
- `task css-watch` - Watch and rebuild CSS

### Configuration Options

During project generation, you can configure:

- **Project name** - Human-readable project name
- **Project slug** - Python package name
- **Database engine** - PostgreSQL or SQLite
- **Use Celery** - Async task processing
- **Use Redis** - Caching and Celery broker
- **Use Sentry** - Error tracking
- **Use Cloudflare Turnstile** - CAPTCHA protection

---

<a name="japanese"></a>
## 🌟 日本語

DjangoにTailwind CSS、Alpine.js、そしてモダンな開発ツールを初期搭載した、すぐに開発を始められるプロジェクトテンプレートです。

### 機能

- 🎨 **TailwindCSS** - Flowbiteコンポーネント付きのユーティリティファーストCSS
- ⚡ **Alpine.js** - 軽量なリアクティブフレームワーク
- 🔐 **カスタムユーザーモデル** - メールアドレス認証対応
- 📊 **ダッシュボード** - チャートと統計情報を含む構築済みダッシュボード
- 🏗️ **モジュラー設定** - 開発/本番環境の設定分離
- 🛠️ **開発ツール** - Pre-commitフック、タスク自動化、Poetry
- 🌐 **多言語対応** - 日本語ロケール設定済み
- 🚀 **本番環境対応** - Celery、Redis、PostgreSQL設定

### クイックスタート

```bash
# cookiecutterをインストール
pip install cookiecutter

# プロジェクトを生成
cookiecutter https://github.com/byteboxjp/django-tailwind-dashboard-template

# プロンプトに従って入力
project_name [My Django Project]: My Awesome App
project_slug [my_awesome_app]:
author_name [Your Name]: 山田太郎
email [your.email@example.com]: yamada@example.com
# ... など

# プロジェクトディレクトリに移動
cd my_awesome_app

# 環境変数を設定
cp .env.example .env
# .envファイルを編集

# Python依存関係をインストール
poetry install

# フロントエンド依存関係をインストール
cd frontend
npm install
cd ..

# マイグレーションを実行
task migrate

# スーパーユーザーを作成
task createsuperuser

# 開発サーバーを起動
task dev

# 別のターミナルでCSSウォッチャーを起動
task css-watch
```

### プロジェクト構造

```
my_awesome_app/
├── my_awesome_app/         # Djangoプロジェクトディレクトリ
│   ├── apps/               # Djangoアプリケーション
│   │   ├── accounts/       # ユーザー認証
│   │   ├── core/          # コア機能
│   │   └── dashboard/     # ダッシュボードビュー
│   ├── config/            # プロジェクト設定
│   │   └── settings/      # モジュラー設定
│   ├── static/            # 静的ファイル
│   └── templates/         # HTMLテンプレート
├── frontend/              # フロントエンドビルドツール
├── .env.example          # 環境変数テンプレート
├── pyproject.toml        # Poetry設定
└── Taskfile.yml          # タスク自動化
```

### 利用可能なタスク

`task --list`で全タスクを確認できます：

- `task dev` - 開発サーバーの起動
- `task migrate` - データベースマイグレーション
- `task test` - テストの実行
- `task format` - コードフォーマット（black/isort）
- `task lint` - リンティングチェック
- `task css-build` - CSSファイルのビルド
- `task css-watch` - CSSの監視と再ビルド

### 設定オプション

プロジェクト生成時に以下を設定できます：

- **プロジェクト名** - 人間が読めるプロジェクト名
- **プロジェクトスラッグ** - Pythonパッケージ名
- **データベースエンジン** - PostgreSQLまたはSQLite
- **Celeryの使用** - 非同期タスク処理
- **Redisの使用** - キャッシュとCeleryブローカー
- **Sentryの使用** - エラートラッキング
- **Cloudflare Turnstileの使用** - CAPTCHA保護

---

## Development Workflow

1. **Pre-commit hooks** are automatically installed
2. **Code formatting** with Black and isort
3. **Linting** with Ruff and Flake8
4. **Security checks** with Bandit
5. **Secret detection** to prevent credential leaks

## Deployment

The template is production-ready with:

- Gunicorn configuration
- PostgreSQL support
- Redis caching
- Celery for async tasks
- Static file handling
- Environment-based settings

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
