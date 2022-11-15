from django.dispatch import receiver
from djoser.signals import user_registered
from expenses.services import create_default_category_for_user


@receiver(user_registered, dispatch_uid='create_user')
def create_user(sender, user, request, **kwargs):
    """Заполняем пользователя остальными данными"""
    data = request.data
    user.first_name = data.get("first_name", "")
    user.last_name = data.get("last_name", "")
    user.save()
    create_default_category_for_user(user)
