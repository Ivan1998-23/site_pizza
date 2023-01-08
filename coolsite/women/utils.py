from django.db.models import Count
from django.core.cache import cache
from .models import *

menu = [{'title': 'О нас', 'url_name': 'about'},
        # {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Замовити', 'url_name': 'contact'}
]


# Mixin позволяет создавать клас где у кажного обьекта бкдкь свои атрибуты

class DataMixin:
    paginate_by = 3
    # Создает контекст для шаблона  по умолчанию
    def get_user_context(self, **kwargs):
        context = kwargs
        # с помощю АРІ низкого уровня считываем с cats
        cats = cache.get('cats')
        # если cats небыл считан с БД то делаем запрос с БД
        if not cats:
            cats = Category.objects.annotate(Count('women'))
            # заносим данные в кеш на 60 секунт
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
