from django.shortcuts import render
from django.urls import reverse_lazy
from requests import post
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .filters import PostFilter, CategoryFilter
from .forms import PostForm
from django.views import View


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import Group
from django.core.cache import cache # импортируем наш кэш
class NewsList(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_template_names(self):
        if self.request.path == '/news/':
            self.template_name = 'post_list.html'
        elif self.request.path == '/news/search/':
            self.template_name == 'search.html'
        return self.template_name


class NewsDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'news-{self.kwargs["pk"]}',None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
        return obj

class NewsSearch(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     if self.request.path == '/articles/create/':
    #         post.post_type = 'AR'
    #     post.save()
    #     if self.request.path == '/create/':
    #         post.post_type = 'NE'
    #     post.save()
    #     return super().form_valid(form)


class NewsUpdate(UpdateView):
    model = Post
    template_name = 'post_edit.html'



class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        return context


class CategoryView(ListView):
    model = Category
    ordering = 'name'
    template_name = 'category/categorys_list.html'
    context_object_name = 'categorys'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CategoryFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class SubscribeToCategoryView(LoginRequiredMixin, View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        user = request.user

        if not category.subscribers.filter(id=user.id).exists():
            category.subscribers.add(user)  # Добавляем пользователя в подписчики категории

            # Проверка, существует ли группа с таким именем
            group_name = category.name  # Название группы — это имя категории
            group, created = Group.objects.get_or_create(name=group_name)

            # Добавление пользователя в группу
            group.user_set.add(user)
            group.save()

        return redirect('categorys_list')  # Перенаправление на список категорий


class UnsubscribeFromCategoryView(LoginRequiredMixin, View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        user = request.user

        if category.subscribers.filter(id=user.id).exists():
            category.subscribers.remove(user)  # Удаляем пользователя из подписчиков категории

            # Удаление пользователя из группы с названием категории
            group_name = category.name
            group = Group.objects.get(name=group_name)
            group.user_set.remove(user)
            group.save()

        return redirect('categorys_list')  # Перенаправление на список категорий


