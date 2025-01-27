from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category, PostCategory
from .tasks import send_new_post_notifications

@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":
        categories = instance.category.all()

        # Собираем подписчиков
        subscribers_emails = set()
        for category in categories:
            subscribers_emails.update(category.subscribers.values_list('email', flat=True))

        # Если есть подписчики, отправляем уведомления
        if subscribers_emails:
            subject = f"Новый пост в категории: {', '.join([cat.name for cat in categories])}"
            from_email = 'Shapch1c@yandex.ru'

            # Генерация HTML и текстовой версии письма
            html_content = render_to_string(
                'category/follow/email/new_post_notification.html',
                {'post': instance, 'categories': categories}
            )
            text_content = f"Заголовок: {instance.title}\n\n" \
                           f"Краткое описание: {instance.preview()}\n\n" \
                           f"Ссылка: http://127.0.0.1:8000{instance.get_absolute_url()}"

            # Создание и отправка email-сообщения
            send_new_post_notifications.delay(
                list(subscribers_emails), subject, text_content, html_content)
