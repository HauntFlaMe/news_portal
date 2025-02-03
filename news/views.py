from django.http import HttpResponse

def index(request):
    return HttpResponse("Добро пожаловать на News Portal!")

from django.shortcuts import get_object_or_404
from .models import Post

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return HttpResponse(f'Заголовок: {post.title}<br>Текст: {post.text}')

from django.shortcuts import get_object_or_404
from .models import Post

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return HttpResponse(f'Заголовок: {post.title}<br>Текст: {post.text}')