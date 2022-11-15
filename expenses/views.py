from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import CategoryUserSerializer, CategorySerializer
from .models import Category
from .paginations import CustomPagination
from .permissions import ReadOnly


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryUserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_staff:
            return queryset
        return queryset.filter(user=user)

    def get_permissions(self):
        if self.request.user.is_staff:
            self.permission_classes += (ReadOnly,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            self.serializer_class = CategorySerializer
        return super().get_serializer_class()
