from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet, TransactionViewSet

router = routers.DefaultRouter()
router.register('category', CategoryViewSet)
router.register('transaction', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
