# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## 📚 ドキュメント

- **開発者向け詳細ガイド**: [CLAUDE.md](CLAUDE.md) - Claude Codeやその他のAIツールでの開発に最適化されたプロジェクトガイド
- **各アプリケーションのガイド**: 各アプリディレクトリ内の`CLAUDE.md`を参照

## 概要

このプロジェクトは、Django + TailwindCSSで構築されたダッシュボードアプリケーションです。

## 機能

- 🔐 カスタムユーザーモデル（メールアドレス認証）
- 📊 ダッシュボード with Chart.js
- 🎨 TailwindCSS + Flowbite UI
- ⚡ Alpine.js for reactive UI
- 🛡️ Cloudflare Turnstile統合（オプション）
- 📧 メール通知機能
- 🌐 多言語対応（日本語設定済み）
- 🚀 Celery + Redisでの非同期処理（オプション）

## 必要な環境

- Python {{ cookiecutter.python_version }}+
- PostgreSQL {{ cookiecutter.postgresql_version }}+ (またはSQLite3)
- Node.js 16+
- Redis（Celery使用時）

## セットアップ

### 1. 環境変数の設定

```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

### 2. Pythonの依存関係をインストール

```bash
poetry install
```

### 3. フロントエンドの依存関係をインストール

```bash
cd frontend
npm install
cd ..
```

### 4. データベースのセットアップ

```bash
# データベースの作成（PostgreSQL使用時）
task create_local_database

# マイグレーションの実行
task migrate

# スーパーユーザーの作成
task createsuperuser
```

### 5. 静的ファイルの収集

```bash
task collectstatic
```

## 開発

### 開発サーバーの起動

```bash
# Djangoサーバー
task dev

# 別のターミナルでTailwindCSSのウォッチ
task css-watch
```

### テストの実行

```bash
# 全てのテストを実行
task test

# 特定のアプリのテストを実行
task test -- apps.accounts

# カバレッジ付きでテストを実行
poetry run pytest --cov=apps --cov-report=html
```

### コードの品質チェック

```bash
# コードフォーマット
task format

# リンティング
task lint

# pre-commitフックの実行
poetry run pre-commit run --all-files
```

## 利用可能なタスク

`task --list`で全てのタスクを確認できます：

- `task dev` - 開発サーバーの起動
- `task test` - テストの実行
- `task migrate` - マイグレーションの実行
- `task shell` - Django shellの起動
- `task format` - コードのフォーマット
- `task lint` - リンティングの実行
- `task css-build` - CSSのビルド
- `task css-watch` - CSSの監視とビルド

## プロジェクト構造

```
{{ cookiecutter.project_slug }}/
├── {{ cookiecutter.project_slug }}/         # Djangoプロジェクト
│   ├── apps/                                # アプリケーション
│   │   ├── accounts/                        # ユーザー認証
│   │   ├── core/                           # 共通機能
│   │   └── dashboard/                      # ダッシュボード
│   ├── config/                             # 設定ファイル
│   │   └── settings/                       # 環境別設定
│   ├── static/                             # 静的ファイル
│   └── templates/                          # HTMLテンプレート
├── frontend/                               # フロントエンドビルドツール
├── tests/                                  # テスト
├── .env.example                           # 環境変数のサンプル
├── pyproject.toml                         # Poetry設定
└── Taskfile.yml                           # タスクランナー設定
```

## デプロイ

本番環境へのデプロイ手順：

1. 環境変数を本番用に設定
2. `DEBUG=False`に設定
3. 静的ファイルを収集: `task collectstatic`
4. Gunicornで起動: `task guni`

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを作成して変更内容について議論してください。