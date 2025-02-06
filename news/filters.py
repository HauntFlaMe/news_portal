import django_filters
from .models import Post
from django import forms

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    author__user__username = django_filters.CharFilter(lookup_expr='icontains', label='Автор')
    created_at = django_filters.DateFilter(
        lookup_expr='gt',
        label='Позже указанной даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at']