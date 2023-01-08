from django.db import models
from django.urls import reverse

# Create your models here.
# verbose_name= для того щоб в адмінке була відповідна назва колонки
class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name = 'Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name = 'Текст статті')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name = 'Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name = 'Час створення')
    time_update = models.DateTimeField(auto_now_add=True, verbose_name = 'Час оновлення')
    is_published = models.BooleanField(default=True, verbose_name = 'Публікація')
    '''Добовляем новый ключ который хависит от таблицы Category
    #первый парамент указывает таблицу куда обращатся
    #on_delete=models.PROTECT что делать в таблице если первичною таблицу удалили
    #запрещает удаление елементов с родительськой таблицы если его используют'''
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,  verbose_name='Категорії')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    #додаємо параметри які будуть відображаися в адмін панелі
    class Meta:
        verbose_name = 'Страви'
        verbose_name_plural = 'Страви'
        #порядок сортування жінок по часу, якщо час однаковий  то по 'title'
        #якщо стоїть  '-title' то сортує навпаки
        ordering = ['time_create', 'title']


#Создаем новую таблицу которая будет иметь информацию про категории
#у нее будет
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name = 'Категорія')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категорію'
        verbose_name_plural = 'Категорія'
        #порядок сортування жінок по часу, якщо час однаковий  то по 'title'
        #якщо стоїть  '-title' то сортує навпаки
        ordering = ['id']
