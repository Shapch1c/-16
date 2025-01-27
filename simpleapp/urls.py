from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, NewsUpdate, NewsDelete, IndexView, CategoryView, UnsubscribeFromCategoryView, SubscribeToCategoryView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='post_list'),
    path('categorys/',CategoryView.as_view(), name='categorys_list'),
    path('category/<int:category_id>/subscribe/', SubscribeToCategoryView.as_view(), name='subscribe_to_category'),
    path('category/<int:category_id>/unsubscribe/', UnsubscribeFromCategoryView.as_view(), name='unsubscribe_from_category'),
    # path('categorys/search/', CategorySearch.as_view(), name='category_search_list'),
    # path('', IndexView.as_view()),
    path('search/', cache_page(300)(NewsSearch.as_view()), name='search'),
    path('<int:pk>/', NewsDetail.as_view(), name='post_detail'),
    path('create/', NewsCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('articles/create/', NewsCreate.as_view(), name='post_create'),
    path('articles/<int:pk>/edit/', NewsUpdate.as_view(), name='post_edit'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
]



