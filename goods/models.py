from django.db import models
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')                                # В админке класс- название таблицы к нему прибывляется S.Можно изменить в классе Meta. Модель поля текст, макс 200, уникальны True категории!
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True, verbose_name='URL')              # модель поля слаг-фрагмент текстового урл адреса,который ведет на соответсвующую котегорию, чтоб не писать для них разные идентификаторы. На латинице! Автоматическое заполнение настроить в админ!

    class Meta:                                              # Можно вносить коррективы в название класса Категории
        db_table = 'category'                                # Так будет называться класс в админке, вмето ()
        verbose_name = 'Категорию'                           # альтернативное имя для db_table
        verbose_name_plural = 'Категории'                    # альтернативное имя для db_table мн.ч
 
    def __str__(self):                                    # что будет отображаться в админке
        return self.name 


class Products(models.Model):
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')                # models.ForeignKey(to=Categories-сзяхали с таблицей категории. CASCADE-при удалении категории удалятся все ее товары. PROTECT-категория не удалится,пока есть товары.
    name = models.CharField(max_length=200, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True, verbose_name='URL')                # Можно без слага. ID каждому товару дается уникальный втоматически.
    description = models.TextField(blank=True, null=True, verbose_name='Описание')                                 # blank=True, null=True,-поле может быть пустым!
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')         # upload_to -хде зранить картинки из базы данных.
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')                 # модель поля DecimalField - с плавающей точкой
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')        
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')                                   # модель поля PositiveIntegerField-положительные целые
    

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",)                   # кортеж. товары сортируются по id

    def __str__(self):
        return f'{self.name} Количество - {self.quantity}'                      # что будет отображаться в админке

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    

    def display_id(self):                                                   # метод к классу продукт self.свойство дополняет айди до 5 знаков выводим в html
        return f"{self.id:05}"


    def sell_price(self):                                                   # высчитывает стоимость товара. 
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)      # если товар имеет скидку цена- скидка
        
        return self.price  