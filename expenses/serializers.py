from django.db import transaction
from django.db.models import F
from rest_framework import serializers
from decimal import Decimal
from .models import Category, Transaction, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'user')


class CategoryUserSerializer(CategorySerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'user', 'category', 'amount', 'organization',
                  'description', 'created_at')

    def validate(self, data):
        """Checking if a category belongs to a user"""
        if data['user'] != data['category'].user:
            raise serializers.ValidationError('The category does not belong to the user')
        return data

    def create(self, validated_data):
        with transaction.atomic():
            transaction_obj = super().create(validated_data)
            self.change_user_balance(user=validated_data['user'],
                                     amount=validated_data['amount'],
                                     operator='+')
        return transaction_obj

    def update(self, instance, validated_data):
        user_old, amount_old = instance.user, instance.amount
        user_new, amount_new = validated_data['user'], validated_data['amount']

        with transaction.atomic():
            if user_old == user_new and amount_old != amount_new:
                amount = amount_old - amount_new
                self.change_user_balance(user=user_new, amount=amount, operator='-')
            elif user_old != user_new:
                self.change_user_balance(user=user_old, amount=amount_old, operator='-')
                self.change_user_balance(user=user_new, amount=amount_new, operator='+')

            transaction_obj = super().update(instance, validated_data)
        return transaction_obj

    @staticmethod
    def change_user_balance(user: User, amount: Decimal, operator: str) -> None:
        if operator == '+':
            user.balance = F('balance') + amount
        elif operator == '-':
            user.balance = F('balance') - amount

        user.save()
        user.refresh_from_db()

        if user.balance < 0:
            raise serializers.ValidationError(f'Insufficient funds on {user} account')
