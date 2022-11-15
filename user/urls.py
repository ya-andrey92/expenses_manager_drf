from django.urls import path
from .views import CustomUserViewSet

urlpatterns = [
    path('', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('me/', CustomUserViewSet.as_view({'get': 'me', 'put': 'me', 'patch': 'me'})),
]
