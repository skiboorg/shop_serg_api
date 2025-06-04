from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.utils.safestring import mark_safe
from .models import *



class ProductImageInline(NestedStackedInline):
    model = ProductImage
    extra = 0

class StyleProductInline(NestedStackedInline):
    model = StyleProduct
    extra = 0

class StyleAdmin(NestedModelAdmin):
    model = Style
    inlines = [StyleProductInline]

class ProductAdmin(NestedModelAdmin):
    list_display = ('image_preview','category','article','name','is_new','is_popular',)
    model = Product
    inlines = [ProductImageInline]
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        main_image = obj.images.filter(is_main=True)
        if main_image.exists():
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(main_image.first().image.url))
        else:
            return 'Нет изображения'

    image_preview.short_description = 'Основное изображение'




admin.site.register(Category)
admin.site.register(Style, StyleAdmin)
admin.site.register(Product, ProductAdmin)

