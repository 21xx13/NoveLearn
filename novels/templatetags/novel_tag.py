from django import template
from novels.models import Category, Novel


register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('novels/tags/last_novels.html')
def get_last_novels(count=5):
    novels = Novel.objects.order_by("id")[:count]
    return {"last_novels": novels}