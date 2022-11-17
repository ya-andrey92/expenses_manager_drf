from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings
from celery import shared_task
from .services import get_statistics

User = get_user_model()


@shared_task(name='send_statistics')
def send_beat_statistics_user_mail() -> None:
    users = User.objects.filter(is_staff=False)
    for user in users:
        data = get_statistics(user)

        if data:
            full_name = f' {user.first_name} {user.last_name}'
            date = data.get('date')

            email = EmailMessage(
                subject=f'Статистика за {date}',
                body=f'Добрый день,{full_name}\n'
                     f'Ваша статистика по доходам/расходам за {date}.',
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )

            email.attach_file(data.get('file'))
            email.send()
