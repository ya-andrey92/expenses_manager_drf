from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'user')


class CategoryUserSerializer(CategorySerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
