# Config - Claude Code ガイド

## 設定ファイル構造

### settings/ ディレクトリ
```
settings/
├── __init__.py    # デフォルトはlocalを読み込み
├── base.py        # 共通設定
├── local.py       # 開発環境
├── production.py  # 本番環境
└── test.py        # テスト環境
```

## 環境別設定の使い分け

### 開発環境 (local.py)
```bash
# デフォルト
python manage.py runserver

# 明示的に指定
python manage.py runserver --settings=config.settings.local
```

### 本番環境 (production.py)
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
gunicorn config.wsgi:application
```

### テスト環境 (test.py)
```bash
pytest  # pytest.ini で自動設定
```

## 主要な設定項目

### base.py - 共通設定
- **INSTALLED_APPS**: アプリケーション登録
- **MIDDLEWARE**: ミドルウェア設定
- **TEMPLATES**: テンプレート設定
- **AUTH_USER_MODEL**: カスタムユーザーモデル
- **LANGUAGE_CODE**: 言語設定（ja）
- **TIME_ZONE**: タイムゾーン（{{ cookiecutter.timezone }}）

### local.py - 開発固有
- **DEBUG = True**
- **EMAIL_BACKEND**: コンソール出力
- **INTERNAL_IPS**: Django Debug Toolbar用

### production.py - 本番固有
- **DEBUG = False**
- **SECURE_SSL_REDIRECT = True**
- **セッション設定**: Redisベース
- **ロギング設定**: ファイル出力
{% if cookiecutter.use_sentry == "y" %}- **Sentry統合**: エラートラッキング{% endif %}

## 環境変数

必須の環境変数（.envファイル）:
```bash
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=example.com,www.example.com
DATABASE_URL=postgres://user:pass@localhost/dbname
```

## カスタム設定の追加

### 新しい設定項目
```python
# base.py に追加
MY_CUSTOM_SETTING = os.getenv("MY_CUSTOM_SETTING", "default_value")

# 使用箇所
from django.conf import settings
value = settings.MY_CUSTOM_SETTING
```

### 環境別オーバーライド
```python
# local.py
from .base import *

MY_CUSTOM_SETTING = "development_value"
```

## トラブルシューティング

### 設定が反映されない
1. `DJANGO_SETTINGS_MODULE`環境変数を確認
2. Pythonパスに`config`が含まれているか確認
3. キャッシュクリア: `find . -name "*.pyc" -delete`

### ImportError
- 循環インポートを避ける
- 設定ファイル内でアプリをインポートしない