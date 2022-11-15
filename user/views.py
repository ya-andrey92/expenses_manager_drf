from djoser.views import UserViewSet
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == 'me' and self.request.method != "DELETE":
            return CustomUserSerializer
        return super().get_serializer_class()
