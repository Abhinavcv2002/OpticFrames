# Generated by Django 5.1.5 on 2025-02-19 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glass', '0002_cart_order_product_delete_gallery_order_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
    ]
