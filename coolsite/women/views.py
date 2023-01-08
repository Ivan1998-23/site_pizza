from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
# Импорт БД
from .models import *
from .utils import *


# title это то что написано на сылке
# menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


class WomenHome(DataMixin, ListView):
    paginate_by = 2
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна сторінка')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


# Create your views here.
# def index(request):
#     # Это класс Women, получает все статти через ALL()
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)

def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О нас'})


#
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    # генерация ошибки "Доступ запрещон"  403 Forbidden
    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Додати страву')
        return dict(list(context.items()) + list(c_def.items()))


# def addpage(request):
#     #Проверка на то что пользователь ввел не правильные данные
#     #Если нажмет отправить но дынные не правильные то он вернет страницу с правильными
#     # строками
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             try:
#                 form.save()
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления поста')
#
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form,  'memu': menu, 'title': "Добавление статьи"})


#def contact(request):
#    return HttpResponse("Обратная связь")

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Замовити")
        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')



# def login(request):
#     return HttpResponse("Авторизация")


# Берем запись из модели Вимен у которого первичный ключь pk
# если не найдена стр. то ошибка 404 (ф-я get_object_or_404)
#
# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     # Параметры которые будут передаватся
#     context = {
#         'post' : post,
#         'menu' : menu,
#         'title' : post.title,
#         'cat_selected' : post.cat_id,
#     }
#     return render(request, 'women/post.html', context=context)


# Создаем клас представлений
class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = "women/post.html"
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return context


# def show_category(request, cat_id):
#     #выбираем с таблицы Women только те у которых   категория общая
#     posts = Women.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#     context = {
#         'posts': posts,
#         'title': 'Отоброжение по рубрикам',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'women/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Реєстрація")
        return dict(list(context.items()) + list(c_def.items()))

    # вызывается при успешной проверки формы регистрации  (успешной регистрации пользователя)
    def form_valid(self, form):
        #добовляем пользователя в БД
        user = form.save()
        #Авторизовует пользователя
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'
    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторризація")
        return dict(list(context.items()) + list(c_def.items()))

    # ф-я если пользователь залогинелся то он переходит на основную страницу
    def get_success_url(self):
        return reverse_lazy('home')

def LogoutUser(request):
    logout(request)
    return redirect('login')