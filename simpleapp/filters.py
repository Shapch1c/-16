from django_filters import FilterSet
from .models import Post, Category


class PostFilter(FilterSet):
   class Meta:
       model = Post
       fields = {
           # поиск по названию
           'title': ['icontains'],
           'author': ['exact'],
           'post_time': ['gt'],  # дата должна быть больше
       }

class CategoryFilter(FilterSet):
   class Meta:
       model = Category
       fields = {
           # поиск по названию
           'name': ['icontains'],
       }