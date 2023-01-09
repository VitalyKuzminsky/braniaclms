# Отправка обратной связи

from celery import shared_task
from django.core.mail import send_mail

from authapp.models import User


@shared_task  # декоратор для подхватывания задачи celery
def send_feedback_mail(message_body: str, message_form: int = None) -> None:  # Принимаем сообщение, от кого должно
    # прийти и само сообщение. Если пользователь авторизован - отдадим его id, если не авторизован, то будет пусто.
    if message_form is not None:
        user_form = User.objects.filter(pk=message_form).first().get_full_name()  # Если не None, то получили полное имя
    else:
        user_form = 'Не авторизованный пользователь'

    # Вызываем форму отправки с параметрами
    send_mail(
        subject=f"Feedback from: {user_form}",  # тема письма
        message=message_body,  # само сообщение
        recipient_list=["support@blms.local"],  # список тех, кому нужно отправить
        from_email='support@blms.local',
        fail_silently=False  # Если что-то пошло не так, он выведет сообщение
    )
