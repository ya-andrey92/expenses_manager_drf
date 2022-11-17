from django.utils import timezone
from django.db.models import Sum, Case, When
from django.conf import settings
from expenses.models import Transaction, User
from decimal import Decimal
import csv
from typing import Dict, List


def get_statistics(user: User) -> Dict | None:
    """Вычисление статистики по доходам/расходам категорий за день"""
    current_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = current_date - timezone.timedelta(days=1)
    end_date = current_date - timezone.timedelta(seconds=1)

    queryset = Transaction.objects.filter(
        user=user, created_at__range=(start_date, end_date)
    )
    queryset = queryset.select_related('category').values('category__name')
    queryset = queryset.annotate(
        spent=Sum(Case(When(amount__lt=0, then='amount'), default=Decimal('0.00'))),
        received=Sum(Case(When(amount__gt=0, then='amount'), default=Decimal('0.00')))
    )

    if queryset:
        statistics_date = start_date.strftime('%d-%m-%Y')
        file_csv = generation_csv(queryset, user, statistics_date)

        data = {
            'date': statistics_date,
            'file': file_csv
        }
        return data


def generation_csv(data: List, user: User, statistics_date: str) -> str:
    """Генерирует файл со статистикой"""
    filename = f'{user.username}_{statistics_date}.csv'
    file = settings.FOLDER_STATISTICS / filename

    with open(file, 'w') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return file
