from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request):


    context = {
        'title': 'SW',                                    # В строке браузера
        'content': "SnowWave",                            # На главной странице поцентру
    }

    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'SW - О нас',
        'content': "О нас",
        'text_on_page': "Интернет-магазин спортивного инвентаря для катания на лыжах и сноубордах. Большой выбор аксессуаров. "
    }

    return render(request, 'main/about.html', context)