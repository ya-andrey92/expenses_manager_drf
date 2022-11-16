from timestamps.models import models, Model
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('user'))

    def __str__(self):
        return f'{self.user} - {self.name}'


class Transaction(Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2,
                                 verbose_name=_('amount'))
    organization = models.CharField(max_length=256, verbose_name=_('organization'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 verbose_name=_('category'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('user'))

    def __str__(self):
        return f'{self.category} - {self.amount}'
