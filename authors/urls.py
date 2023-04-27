from django.urls import path
from .views import *
app_name = "authors"

urlpatterns = [
   path('', home, name="home"),
   path('news', PostsList.as_view(), name="posts"),
   path('news/search/', PostsSearch.as_view(), name="search"),
   path('news/<int:pk>', PostDetail.as_view(), name="post"),

   path('news/create/', NewsCreate.as_view(),name='news-create'),
   path('article/create/', NewsCreate.as_view(),name='article-create'),

   path('news/edit/<int:pk>', PostFormView.as_view(), name='news-edit'),
   path('article/edit/<int:pk>', PostFormView.as_view(), name='article-edit'),

   path('news/delete/<int:pk>', PostDeleteView.as_view(), name='news-delete'),
   path('article/delete/<int:pk>', PostDeleteView.as_view(), name='article-delete'),

   path('subscribe', Subscribe.as_view(), name = 'subscribe')
]