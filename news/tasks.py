from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Subscription, Post


@shared_task
def notify_subscribers(post_id):
    post = Post.objects.get(id=post_id)
    category = post.categories.first()  # Получаем первую категорию статьи
    if category:
        subscribers = Subscription.objects.filter(category=category)
        for subscription in subscribers:
            subject = f'Новая статья в категории {category.name}'
            message = (
                f'Здравствуйте, {subscription.user.username}!\n\n'
                f'Новая статья: {post.title}\n'
                f'Краткое содержание: {post.preview()}\n\n'
                f'Читать статью: {settings.SITE_URL}{reverse("post_detail", args=[post.id])}'
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.user.email],
            )

@shared_task
def send_weekly_newsletter():
    one_week_ago = timezone.now() - timezone.timedelta(days=7)
    new_posts = Post.objects.filter(created_at__gte=one_week_ago, type='AR')

    for subscription in Subscription.objects.all():
        posts_in_category = new_posts.filter(categories=subscription.category)
        if posts_in_category.exists():
            subject = f'Новые статьи в категории {subscription.category.name} за неделю'
            message = 'Новые статьи:\n\n'
            for post in posts_in_category:
                message += f'{post.title}\n{settings.SITE_URL}{post.get_absolute_url()}\n\n'
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscription.user.email],
            )                        