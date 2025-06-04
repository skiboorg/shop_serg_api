from rest_framework import exceptions, serializers, status, generics


from .models import *
from django.conf import settings



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'




class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True,required=False,read_only=True)
    cat_slug = serializers.SerializerMethodField()
    cat_name = serializers.SerializerMethodField()
    exclude = ['description_editor']

    class Meta:
        model = Product
        fields = '__all__'
    def get_cat_slug(self,obj):
        return obj.category.slug
    def get_cat_name(self,obj):
        return obj.category.name


class ProductShortSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    cat_slug = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id',
            'cat_slug',
            'article',
            'is_new',
            'is_in_stock',
            'image',
            'name',
            'slug',
            'price',
            'short_description'

        ]
    def get_image(self,obj):
        main_image = obj.images.filter(is_main=True)
        if main_image.exists():
            return f'{settings.IMG_URL}{main_image.first().image.url}'
        else:
            return None

    def get_cat_slug(self,obj):
        return obj.category.slug

class StyleProductSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(many=False,read_only=True)
    class Meta:
        model = StyleProduct
        fields = '__all__'

class StyleSerializer(serializers.ModelSerializer):
    products = StyleProductSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Style
        fields = '__all__'

class StyleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = '__all__'









class CategorySerializer(serializers.ModelSerializer):
    products = ProductShortSerializer(many=True)
    class Meta:
        model = Category
        fields = '__all__'


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['image','name','slug','short_description','display_amount']
