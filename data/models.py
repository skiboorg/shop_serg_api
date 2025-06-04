from django.db import models
from django_resized import ResizedImageField
from django_ckeditor_5.fields import CKEditor5Field
from shop.models import Product



class Banner(models.Model):
    order_num = models.IntegerField(default=10)
    image_big = ResizedImageField('Баннер десктоп', size=[1440, 640], quality=95, force_format='WEBP', upload_to='banner/images',
                              blank=False, null=True)
    image_small = ResizedImageField('Баннер мобилка', size=[760, 640], quality=95, force_format='WEBP',
                                 upload_to='banner/images',
                                 blank=False, null=True)
    text_big = models.TextField('Текст большой', blank=True, null=True)
    text_small = models.TextField('Текст маленький', blank=True, null=True)
    def __str__(self):
        return f'{self.order_num}'



    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['order_num']

