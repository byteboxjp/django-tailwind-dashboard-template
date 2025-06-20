# Dashboard App - Claude Code ガイド

## 概要
管理ダッシュボードとデータ可視化を提供するアプリケーション。

## 主要機能

### Views (`views/index.py`)
- **DashboardIndexView**: メインダッシュボード
  - 統計情報の集計
  - Chart.js用データの準備
  - リアルタイムメトリクス

### Models (`models.py`)
- **Activity**: ユーザーアクティビティログ
  - アクション追跡
  - IPアドレス記録
  - タイムスタンプ

### テンプレート構造
```
templates/dashboard/
├── base.html       # ダッシュボードレイアウト
└── index.html      # メインダッシュボード
```

## JavaScript統合

### Chart.js データ形式
```javascript
// views/index.py で生成されるデータ
{
    labels: ['01/10', '01/11', ...],
    datasets: [{
        label: '新規ユーザー',
        data: [5, 10, 8, ...],
        borderColor: 'rgb(59, 130, 246)'
    }]
}
```

### Alpine.js コンポーネント
```html
<div x-data="dashboardStats">
    <!-- 統計情報の動的更新 -->
</div>
```

## カスタマイズ例

### 新しい統計追加
```python
# views/index.py
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['new_metric'] = MyModel.objects.count()
    return context
```

### 新しいチャート追加
1. `views/index.py`でデータ準備
2. `templates/dashboard/index.html`でChart.js設定
3. `static/js/main.js`で初期化

## パフォーマンス最適化
- `select_related()`でクエリ削減
- 統計情報のキャッシュ（Redisを使用）
- 非同期データ更新（API経由）