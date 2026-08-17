from rest_framework import serializers
from .models import Furniture, Order


class FurnitureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Furniture

        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order

        fields = "__all__"
