from django.apps import AppConfig

#Конфігурація приложенія до Women
class WomenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
    # алтернативна назва в адмінке програми  Women
    verbose_name = 'Меню'
