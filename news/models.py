from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView
from .models import Post, Category


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Суммарный рейтинг статей автора, умноженный на 3
        post_rating = sum(post.rating for post in self.post_set.all()) * 3

        # Суммарный рейтинг комментариев автора
        comment_rating = sum(comment.rating for comment in self.user.comment_set.all())

        # Суммарный рейтинг комментариев к статьям автора
        post_comment_rating = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())

        # Общий рейтинг автора
        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title} - {self.category.name}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.user.username} - {self.text[:20]}'


class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.type = 'NW'  # Указываем тип "новость"
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    model = Post
    fields = ['title', 'text', 'categories']
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} подписан на {self.category.name}'