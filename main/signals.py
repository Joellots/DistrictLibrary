from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Book, Publisher, Genre, Author
from .utils import send_telegram_message
from django.conf import settings

@receiver(post_save, sender=Book)
def send_book_added_message(sender, instance, created, **kwargs):
    if created:
        message = f'New Book added: {instance.title}\nNumber of Pages: {instance.pages}\nRating: {instance.rating}\nDate Published: \
        {instance.published_date}\nPublisher: {instance.publisher}\nGenre: {instance.genre}\nAuthor: {instance.author}'
        send_telegram_message(settings.DEFAULT_CHAT_ID, message)

@receiver(pre_delete, sender=Book)
def send_book_deleted_message(sender, instance, **kwargs):
    message = f'The Book "{instance.title}" has been deleted.'
    send_telegram_message(settings.DEFAULT_CHAT_ID, message)

@receiver(pre_delete, sender=Publisher)
def send_publisher_deleted_message(sender, instance, **kwargs):
    message = f'The Publisher "{instance.name}" has been deleted.'
    send_telegram_message(settings.DEFAULT_CHAT_ID, message)

@receiver(pre_delete, sender=Genre)
def send_genre_deleted_message(sender, instance, **kwargs):
    message = f'The Genre "{instance.name}" has been deleted.'
    send_telegram_message(settings.DEFAULT_CHAT_ID, message)

@receiver(pre_delete, sender=Author)
def send_author_deleted_message(sender, instance, **kwargs):
    message = f'The Author "{instance.Full_Name}" has been deleted.'
    send_telegram_message(settings.DEFAULT_CHAT_ID, message)

# @receiver(post_save, sender=Comment)
# def send_comment_posted_message(sender, instance, created, **kwargs):
#     if created:
#         message = f'New comment on "{instance.product.name}" by {instance.author}: {instance.text[:100]}'
#         send_telegram_message(settings.DEFAULT_CHAT_ID, message)

