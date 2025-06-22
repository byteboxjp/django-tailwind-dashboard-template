"""
Core template tags and filters.
"""
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
import json

register = template.Library()


@register.filter
def addclass(field, css_class):
    """
    フォームフィールドにCSSクラスを追加
    
    Usage:
        {% raw %}{{ form.field|addclass:"form-input" }}{% endraw %}
    """
    return field.as_widget(attrs={"class": css_class})


@register.filter
def placeholder(field, text):
    """
    フォームフィールドにプレースホルダーを追加
    
    Usage:
        {% raw %}{{ form.field|placeholder:"メールアドレスを入力" }}{% endraw %}
    """
    return field.as_widget(attrs={"placeholder": text})


@register.simple_tag
def site_name():
    """
    サイト名を返す
    
    Usage:
        {% raw %}{% site_name %}{% endraw %}
    """
    return getattr(settings, 'SITE_NAME', 'DTD')


@register.simple_tag
def get_setting(name, default=None):
    """
    Django設定値を取得
    
    Usage:
        {% raw %}{% get_setting "DEBUG" %}
        {% get_setting "CUSTOM_SETTING" "default_value" %}{% endraw %}
    """
    return getattr(settings, name, default)


@register.inclusion_tag('core/pagination.html')
def pagination(page_obj, **kwargs):
    """
    ページネーションコンポーネントを表示
    
    Usage:
        {% raw %}{% pagination page_obj %}{% endraw %}
    """
    from apps.core.utils import get_page_range
    
    return {
        'page_obj': page_obj,
        'page_range': get_page_range(page_obj),
        **kwargs
    }


@register.filter
def json_dumps(data):
    """
    PythonオブジェクトをJSON文字列に変換
    
    Usage:
        <script>
            const data = {% raw %}{{ python_dict|json_dumps|safe }}{% endraw %};
        </script>
    """
    return mark_safe(json.dumps(data, ensure_ascii=False))


@register.filter
def multiply(value, arg):
    """
    数値を掛け算
    
    Usage:
        {% raw %}{{ price|multiply:quantity }}{% endraw %}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """
    数値を割り算
    
    Usage:
        {% raw %}{{ total|divide:count }}{% endraw %}
    """
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.simple_tag(takes_context=True)
def active_class(context, url_name, css_class='active'):
    """
    現在のURLと一致する場合にCSSクラスを返す
    
    Usage:
        <li class="{% raw %}{% active_class 'home' 'active' %}{% endraw %}">
    """
    request = context.get('request')
    if not request:
        return ''
    
    from django.urls import reverse, resolve
    
    try:
        current_url_name = resolve(request.path).url_name
        if current_url_name == url_name:
            return css_class
    except:
        pass
    
    return ''


@register.filter
def get_item(dictionary, key):
    """
    辞書から値を取得
    
    Usage:
        {% raw %}{{ my_dict|get_item:key }}{% endraw %}
    """
    return dictionary.get(key)