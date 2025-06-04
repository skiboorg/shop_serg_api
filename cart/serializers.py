from rest_framework import serializers
from .models import *
from shop.serializers import ProductShortSerializer
from django.conf import settings

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    total_price = serializers.ReadOnlyField()
    def get_image(self, obj):
        if obj.product.images:
            return settings.IMG_URL + obj.product.images.filter(is_main=True).first().image.url
        else:
            return None
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Cart
        fields = [
            'items',
            'total_price',
            'items_count'
        ]
