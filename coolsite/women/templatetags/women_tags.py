from django import template
from women.models import *
from women.views import menu

#створення користувацього тега
register = template.Library()

# за допомогою @register.simple_tag() створюємо
# новий тег із ф-ї # Декоратор
# name = 'getcats' для того чтобы вызывать не  ф-ю get_categories а переменную
@register.simple_tag( name = 'getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)
@register.simple_tag(name = 'getmenu')
def get_menu():
    return menu

#включающие теги
#дозаоляє повертати фрагмент HTML
#list_categories.html це шаблон який буде повертатися
@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, 'cat_selected': cat_selected}

#включающие теги
#дозаоляє повертати фрагмент HTML
#list_categories.html це шаблон який буде повертатися
@register.inclusion_tag('women/list_menu.html')
def show_menu():
    return {"menu": menu}