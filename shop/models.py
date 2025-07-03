from django.db import models
from pytils.translit import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField

class Style(models.Model):
    order_num = models.IntegerField(default=1, null=True)
    style = models.CharField(default='col-span-12 md:col-span-4',
                             help_text='col-span-12 md:col-span-9 md:col-start-4, '
                                       'col-span-12 md:col-span-4 md:col-start-2, '
                                       'col-span-12 md:col-span-4 md:col-start-9'
                                       'col-span-12 md:col-span-6',
                             blank=False,  max_length=255)
    image = models.FileField(upload_to='shop/category/images', blank=True, null=True)
    price = models.DecimalField('Цена', default=0, decimal_places=2, max_digits=10, blank=True)
    name = models.CharField('Название', max_length=255, blank=True, null=False)
    slug = models.CharField('ЧПУ', max_length=255,blank=True, null=True)
    html_content = CKEditor5Field('SEO текст', blank=True, null=False)


    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('order_num',)
        verbose_name = 'Стиль'
        verbose_name_plural = 'Стиль'

class Category(models.Model):
    order_num = models.IntegerField(default=1, null=True)
    image = models.FileField(upload_to='shop/category/images', blank=True, null=True)

    name = models.CharField('Название', max_length=255, blank=True, null=False)
    slug = models.CharField('ЧПУ', max_length=255,blank=True, null=True)
    short_description = models.TextField('Короткое описание', blank=True, null=False)
    html_content = CKEditor5Field('SEO текст', blank=True, null=False)
    display_amount = models.IntegerField(default=0, blank=True, null=True)
    styles = models.ManyToManyField(Style, blank=True)


    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('order_num',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



class Product(models.Model):
    order_num = models.IntegerField(default=1, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    article = models.CharField('Артикул', max_length=20,blank=True, null=True)

    price = models.DecimalField('Цена', default=0, decimal_places=2,max_digits=10, blank=True)

    is_new = models.BooleanField('Новинка', default=False, null=False)
    is_in_stock = models.BooleanField('В наличии?', default=True, null=False)
    is_popular = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    slug = models.CharField('ЧПУ',max_length=255,
                            help_text='Если не заполнено, создается на основе поля Назавание',
                            blank=True, null=True, editable=False)
    short_description = models.TextField('Короткое описание', blank=True, null=False)
    editor_1 = CKEditor5Field('Свойства', blank=True, null=True, config_name='extends')
    editor_2 = CKEditor5Field('Применеие', blank=True, null=True, config_name='extends')
    editor_3 = CKEditor5Field('Состав', blank=True, null=True, config_name='extends')
    editor_4 = CKEditor5Field('Доствка', blank=True, null=True, config_name='extends')
    editor_5 = CKEditor5Field('Результат', blank=True, null=True, config_name='extends')



    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('order_num',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False,
                                related_name='images')
    image = ResizedImageField(size=[1500, 1500], quality=95, force_format='WEBP', upload_to='shop/product/images',
                              blank=False, null=True)
    is_main = models.BooleanField('Основное', default=False, null=False)

    def __str__(self):
        return f''

    class Meta:

        verbose_name = 'Доп. изображение товара'
        verbose_name_plural = 'Доп. изображения товара'



class StyleProduct(models.Model):
    order_num = models.IntegerField(default=1, null=True)
    style = models.ForeignKey(Style, on_delete=models.CASCADE, null=True, blank=False,related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        ordering = ('order_num',)
        verbose_name = 'Товар стиля'
        verbose_name_plural = 'Товар стиля'
