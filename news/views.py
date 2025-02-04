from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404


def index(request):
    return HttpResponse("Добро пожаловать на News Portal!")


def news_list(request):
    posts = Post.objects.filter(type='NW').order_by('-created_at')  # Только новости, отсортированные по дате
    return render(request, 'news/news_list.html', {'posts': posts})


def news_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'news/news_detail.html', {'post': post})
