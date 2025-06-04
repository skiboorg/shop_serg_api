from rest_framework import serializers
from .models import *
from shop.serializers import ProductShortSerializer


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

