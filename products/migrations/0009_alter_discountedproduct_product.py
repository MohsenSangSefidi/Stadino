# Generated by Django 5.1.4 on 2025-05-19 08:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_favoriteproducts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountedproduct',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='discounted_products', to='products.product'),
        ),
    ]
