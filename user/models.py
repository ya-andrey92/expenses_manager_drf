from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_('email address'))
    balance = models.DecimalField(max_digits=11, decimal_places=2, default=0,
                                  validators=[MinValueValidator(limit_value=0)],
                                  verbose_name=_('balance'))
