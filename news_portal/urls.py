"""
URL configuration for news_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from .views import (NewsCreateView, NewsUpdateView, NewsDeleteView,
                    ArticleCreateView, ArticleUpdateView, ArticleDeleteView)

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка Django
    path('', include('news.urls')),   # Подключение URL-адресов приложения news
]

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
]

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news/<int:post_id>/', views.news_detail, name='news_detail'),
]

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news/<int:post_id>/', views.news_detail, name='news_detail'),
    path('news/search/', views.news_search, name='news_search'),
]

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news/<int:post_id>/', views.news_detail, name='news_detail'),
    path('news/search/', views.news_search, name='news_search'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]