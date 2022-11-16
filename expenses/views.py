from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategoryUserSerializer, CategorySerializer, TransactionSerializer
from .models import Category, Transaction
from .paginations import CustomPagination
from .permissions import ReadOnly
from .filters import IsAdminFullOrIsOwnerFilterBackend, TransactionFilter


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryUserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = [IsAdminFullOrIsOwnerFilterBackend]

    def get_permissions(self):
        if self.request.user.is_staff:
            self.permission_classes += (ReadOnly,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            self.serializer_class = CategorySerializer
        return super().get_serializer_class()


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = CustomPagination
    filter_backends = (IsAdminFullOrIsOwnerFilterBackend,
                       DjangoFilterBackend,
                       OrderingFilter)
    filterset_class = TransactionFilter
    ordering_fields = ('amount', 'created_at')

    def get_permissions(self):
        if not self.request.user.is_staff:
            self.permission_classes = (IsAuthenticated, ReadOnly)
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        with transaction.atomic():
            TransactionSerializer.change_user_balance(instance.user, instance.amount, '-')
            response = super().destroy(request, *args, **kwargs)
        return response
