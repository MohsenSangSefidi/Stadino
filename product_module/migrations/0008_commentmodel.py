# Generated by Django 5.0.3 on 2024-04-01 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0007_productmodel_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن پیام')),
                ('rating', models.IntegerField(verbose_name='امتیاز')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.productmodel', verbose_name='کتاب')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.commentmodel', verbose_name='پاسخ')),
            ],
        ),
    ]
