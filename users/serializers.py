from rest_framework import serializers

from .models import BasketItem, BasketModel


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = []

    def to_representation(self, instance):
        item_list = f'{instance.product} x {instance.quantity}'

        representation = super().to_representation(instance)
        representation['item_list'] = item_list
        return representation


class BasketUpdateSerializer(serializers.ModelSerializer):
    order = serializers.CharField(source='id')

    class Meta:
        model = BasketModel
        fields = ['order', ]


class BasketSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    user_address = serializers.CharField(source='user.address', read_only=True)
    items = BasketItemSerializer(many=True)

    def to_representation(self, instance):
        order_num = instance.id
        order = order_num

        representation = super().to_representation(instance)
        representation['order'] = order
        return representation

    class Meta:
        model = BasketModel
        fields = ['items', 'user_first_name', 'user_last_name', 'user_address']
