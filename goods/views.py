from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render

from goods.models import Products
from goods.utils import q_search


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)             # переменная в которую будет передавать QuerySet элементы из бд. GET-словарь,применяем метод словарей get.значение по ключу-page, если не будет ключа,то по умолчанию зн 1.
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)
    
    if category_slug == "all":
        goods = Products.objects.all()              # переменная в которую будет передавать QuerySet все элементы из бд 
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))            # category-форинкей! Показывает товары по категориям. Если в категории нет товаров-вернет 404

    if on_sale:
        goods = goods.filter(discount__gt=0)  

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)             # погинатор по 3 товара на страницу.Импорт!
    current_page = paginator.page(int(page))

    context = {
        "title": "SW - Каталог",                           
        "goods": current_page,                        # нов ключ . Можно "goods": Products.objects.all()
        "slug_url": category_slug
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    context = {"product": product}

    return render(request, "goods/product.html", context=context)
