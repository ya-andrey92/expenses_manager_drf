from rest_framework.filters import BaseFilterBackend
from django_filters import filters, FilterSet
from .models import Transaction


class IsAdminFullOrIsOwnerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.is_staff:
            return queryset
        return queryset.filter(user=user)


class TransactionFilter(FilterSet):
    created_date = filters.DateFromToRangeFilter(field_name='created_at',
                                                 label='created_date')
    created_time = filters.TimeRangeFilter(field_name='created_at__time',
                                           label='created_time')

    class Meta:
        model = Transaction
        fields = {'amount': ['exact', 'gt', 'lt']}
