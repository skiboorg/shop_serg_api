# Generated by Django 5.2.1 on 2025-05-25 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_style_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='style',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='Цена'),
        ),
    ]
