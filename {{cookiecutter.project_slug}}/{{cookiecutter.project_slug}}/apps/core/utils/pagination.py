"""
Pagination utility functions.
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def paginate_queryset(queryset, page_number, per_page=None):
    """
    クエリセットをページネーションする
    
    Args:
        queryset: ページネーションするクエリセット
        page_number: ページ番号
        per_page: 1ページあたりのアイテム数（省略時は設定値を使用）
    
    Returns:
        Page object
    """
    if per_page is None:
        per_page = getattr(settings, 'PAGINATION_PER_PAGE', 20)
    
    paginator = Paginator(queryset, per_page)
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # ページ番号が整数でない場合は1ページ目を返す
        page = paginator.page(1)
    except EmptyPage:
        # ページ番号が範囲外の場合は最後のページを返す
        page = paginator.page(paginator.num_pages)
    
    return page


def get_page_range(page, on_each_side=3, on_ends=2):
    """
    現在のページを中心としたページ番号のリストを取得
    
    Args:
        page: 現在のPageオブジェクト
        on_each_side: 現在のページの前後に表示するページ数
        on_ends: 最初と最後に表示するページ数
    
    Returns:
        ページ番号のリスト（省略部分はNone）
    """
    paginator = page.paginator
    
    if paginator.num_pages <= (on_each_side + on_ends) * 2:
        # ページ数が少ない場合はすべて表示
        return list(range(1, paginator.num_pages + 1))
    
    page_range = []
    
    # 最初のページ
    page_range.extend(range(1, on_ends + 1))
    
    # 現在のページの前後
    if page.number > on_each_side + on_ends + 1:
        page_range.append(None)  # 省略記号
    
    start = max(on_ends + 1, page.number - on_each_side)
    end = min(page.number + on_each_side + 1, paginator.num_pages - on_ends + 1)
    page_range.extend(range(start, end))
    
    # 最後のページ
    if page.number < paginator.num_pages - on_each_side - on_ends:
        page_range.append(None)  # 省略記号
    
    page_range.extend(range(paginator.num_pages - on_ends + 1, paginator.num_pages + 1))
    
    return page_range