from django.http import HttpResponse
from django.shortcuts import render
from .models import Post, Category, Subscription
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .filters import PostFilter
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from .tasks import notify_subscribers


def index(request):
    return HttpResponse("Добро пожаловать на News Portal!")


def news_list(request):
    posts = Post.objects.filter(type='NW').order_by('-created_at')  # Только новости, отсортированные по дате
    return render(request, 'news/news_list.html', {'posts': posts})


def news_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'news/news_detail.html', {'post': post})


def news_list(request):
    posts_list = Post.objects.filter(type='NW').order_by('-created_at')  # Только новости, отсортированные по дате
    paginator = Paginator(posts_list, 10)  # 10 новостей на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_list.html', {'page_obj': page_obj})


def news_search(request):
    posts = Post.objects.filter(type='NW').order_by('-created_at')
    post_filter = PostFilter(request.GET, queryset=posts)
    return render(request, 'news/news_search.html', {'filter': post_filter})


class NewsCreateView(CreateView):
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.type = 'NW'
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class NewsUpdateView(UpdateView):
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')

class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')

class ArticleCreateView(CreateView):
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'news/article_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.type = 'AR'
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class ArticleUpdateView(UpdateView):
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'news/article_edit.html'
    success_url = reverse_lazy('news_list')

class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('news_list')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'profile_edit.html'  # Укажите ваш шаблон
    success_url = reverse_lazy('profile')  # Укажите URL для перенаправления после успешного редактирования

    def get_object(self, queryset=None):
        return self.request.user  # Редактируем профиль текущего пользователя
    
@login_required
def become_author(request):
    authors_group = Group.objects.get(name='authors')
    request.user.groups.add(authors_group)  # Добавляем пользователя в группу 'authors'
    return redirect('profile')  # Перенаправляем на страницу профиля    

@login_required
def subscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    Subscription.objects.get_or_create(user=request.user, category=category)
    return redirect('category_detail', category_id=category_id)

@login_required
def unsubscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    Subscription.objects.filter(user=request.user, category=category).delete()
    return redirect('category_detail', category_id=category_id)

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        notify_subscribers.delay(self.object.id)  # Асинхронный вызов задачи
        return response