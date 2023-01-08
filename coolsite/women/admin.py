from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

#Допоміжний клас який дозволяє відображати інфу про жінок з
# усіма відповідними тегами
class WomenAdmin(admin.ModelAdmin):
    # список палів які хочемор бачити в адмінці
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    # які поял можемо клікнути та перейти
    list_display_links = ('id', 'title')
    # по яким полям можна робити пошук
    search_fields = ('title', 'content')
    #список полей які можна буде редагувати
    list_editable = ('is_published',)
    #по чому можемо фільтрувати
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Мініатюра"

class CategoryAdmin(admin.ModelAdmin):
    # список палів які хочемор бачити в адмінці
    list_display = ('id', 'name')
    # які поля можемо клікнути та перейти
    list_display_links = ('id', 'name')
    # по яким полям можна робити пошук, ставимо " , " бо треба передати кортеж
    search_fields = ('name',)
    #автоматически заполняет слаг на основе name
    prepopulated_fields = {"slug": ("name",)}


#реєструємо моделі
admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ панель о еде'
admin.site.site_header = 'Адмін панель о стравах'