"""
Dashboard index view.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.accounts.models import User
from apps.core.models import Contact


@login_required
def dashboard_index(request):
    """
    ダッシュボードのメインページ
    """
    # 統計情報を取得
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    context = {
        # ユーザー統計
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(last_login__gte=week_ago).count(),
        'new_users_this_month': User.objects.filter(date_joined__gte=month_ago).count(),
        
        # お問い合わせ統計
        'total_contacts': Contact.objects.count(),
        'new_contacts': Contact.objects.filter(status='new').count(),
        'in_progress_contacts': Contact.objects.filter(status='in_progress').count(),
        
        # 最近のお問い合わせ
        'recent_contacts': Contact.objects.filter(
            status__in=['new', 'in_progress']
        ).select_related('user', 'assigned_to').order_by('-created_at')[:5],
        
        # グラフ用データ（最近7日間の新規ユーザー数）
        'user_chart_data': get_user_registration_chart_data(days=7),
    }
    
    return render(request, 'dashboard/index.html', context)


def get_user_registration_chart_data(days=7):
    """
    ユーザー登録数のグラフデータを取得
    """
    data = []
    today = timezone.now().date()
    
    for i in range(days):
        date = today - timedelta(days=i)
        count = User.objects.filter(
            date_joined__date=date
        ).count()
        data.append({
            'date': date.strftime('%m/%d'),
            'count': count
        })
    
    # 日付順に並び替え
    data.reverse()
    
    return data