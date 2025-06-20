# Core App - Claude Code ガイド

## 概要
プロジェクト全体で使用される共通機能とユーティリティを提供。

## 主要コンポーネント

### Abstract Models (`models/base.py`)
```python
# 使用例
from apps.core.models import TimeStampedModel

class MyModel(TimeStampedModel):
    # created_at, updated_at が自動追加
    pass
```

利用可能な抽象モデル:
- **TimeStampedModel**: タイムスタンプ自動管理
- **UUIDModel**: UUID主キー
- **SoftDeleteModel**: 論理削除（deleted_atフィールド）
- **PublishableModel**: 公開状態管理
- **OrderableModel**: 順序管理

### ページ管理 (`models/pages.py`)
- **Page**: 静的ページ（利用規約、プライバシーポリシー等）
- **FAQ**: よくある質問
- **Contact**: お問い合わせ

### ユーティリティ (`utils/`)
- **files.py**: ファイル操作（ユニークファイル名生成、サイズ検証）
- **email.py**: メール送信ヘルパー
- **pagination.py**: ページネーション設定

{% if cookiecutter.use_cloudflare_turnstile == "y" %}### Turnstile統合 (`turnstile.py`)
```python
from apps.core.turnstile import TurnstileMixin

class MyForm(TurnstileMixin, forms.Form):
    # Turnstileフィールドが自動追加
    pass
```{% endif %}

### テンプレートタグ (`templatetags/core_tags.py`)
```django
{% load core_tags %}
{% settings_value "SITE_NAME" %}  {# 設定値取得 #}
```

## 共通パターン

### モデル作成時
```python
from apps.core.models import TimeStampedModel, UUIDModel

class Article(TimeStampedModel, UUIDModel):
    title = models.CharField(max_length=200)
    # id (UUID), created_at, updated_at が自動追加
```

### ソフトデリート使用
```python
from apps.core.models import SoftDeleteModel

class Document(SoftDeleteModel):
    name = models.CharField(max_length=100)
    
# 使用方法
doc = Document.objects.create(name="test")
doc.delete()  # 論理削除（deleted_atをセット）
doc.restore()  # 復元
```

## マイグレーション注意点
- 抽象モデルを継承した場合、各アプリでマイグレーションが必要
- `makemigrations`は各アプリで個別に実行