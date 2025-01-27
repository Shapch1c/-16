from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from simpleapp.models import Category
@shared_task
def send_new_post_notifications(subscribers_emails, subject, text_content, html_content):
    from_email = 'Shapch1c@yandex.ru'
    msg = EmailMultiAlternatives(subject, text_content, from_email, subscribers_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def send_weekly_newsletter():
    today = now()
    week_ago = today - timedelta(days=7)
    categories = Category.objects.all()
    category_news = {}

    for category in categories:
        new_posts = category.post_set.filter(post_time__gte=week_ago)
        if new_posts.exists():
            posts = [
                f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
                f'{post.title}</a>'
                for post in new_posts
            ]
            category_news[category.name] = posts

    if category_news:
        email_body = ""
        for category, posts in category_news.items():
            email_body += f"<h3>Категория: {category}</h3><ul>"
            email_body += "".join(f"<li>{post}</li>" for post in posts)
            email_body += "</ul><br>"

        # Список подписчиков
        subscribers = set(
            subscriber.email
            for category in categories
            for subscriber in category.subscribers.all()
        )

        # Отправляем письмо
        if subscribers:
            send_mail(
                subject="Еженедельная рассылка новостей",
                message="",
                from_email="Shapch1c@yandex.ru",
                recipient_list=list(subscribers),
                html_message=email_body
            )