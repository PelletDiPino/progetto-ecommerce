# Generated by Django 4.1 on 2022-08-29 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_category_slug_alter_product_slug_vendorreview_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendorreview',
            name='text',
        ),
    ]
