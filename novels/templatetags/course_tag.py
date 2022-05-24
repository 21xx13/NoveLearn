from django import template
from novels.models import CourseTheme, CourseSlide


register = template.Library()


@register.simple_tag()
def get_themes():
    """Вывод всех категорий"""
    return CourseTheme.objects.order_by("number")


# @register.inclusion_tag('novels/tags/last_novels.html')
# def get_last_novels(count=5):
#     novels = Novel.objects.order_by("id")[:count]
#     return {"last_novels": novels}