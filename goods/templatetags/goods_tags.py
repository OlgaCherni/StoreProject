from django import template
from django.utils.http import urlencode


from goods.models import Categories


register = template.Library()          # register! Зарегестрировали шаблонный тег.


@register.simple_tag()                  # декоротов в котором используется метод симпл тег, чтоб зарегестрировать функцию, которая будет работать в html, как шаблонный тег
def tag_categories():                   #  Функция, которая возвращает категории(кверисетом из БД). Можно получать инфу из БД по шаблонному тегу в обход контролеров
    return Categories.objects.all()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):                    # для html. доступны переменные из вьюхи через context
    query = context['request'].GET.dict()
    # example with other context vars
    # print(context['title'])
    # print(context['slug_url'])
    # print(context['goods'])
    # print([product.name for product in context['goods']])
    query.update(kwargs)
    return urlencode(query)