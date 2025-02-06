from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import Post, Subscription

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:  # Если пользователь только что создан
        common_group = Group.objects.get(name='common')
        instance.groups.add(common_group)  # Добавляем пользователя в группу 'common'

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.type == 'AR':  # Если создана новая статья
        category = instance.categories.first()  # Получаем первую категорию статьи
        if category:
            subscribers = Subscription.objects.filter(category=category)
            for subscription in subscribers:
                subject = f'Новая статья в категории {category.name}'
                message = (
                    f'Здравствуйте, {subscription.user.username}!\n\n'
                    f'Новая статья: {instance.title}\n'
                    f'Краткое содержание: {instance.preview()}\n\n'
                    f'Читать статью: {settings.SITE_URL}{reverse("post_detail", args=[instance.id])}'
                )
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscription.user.email],
                )

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать в News Portal!'
        message = (
            f'Здравствуйте, {instance.username}!\n\n'
            'Спасибо за регистрацию на нашем сайте.\n'
            'Теперь вы можете читать новости и статьи, а также подписываться на категории.\n\n'
            'С уважением,\nКоманда News Portal'
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
        )                        