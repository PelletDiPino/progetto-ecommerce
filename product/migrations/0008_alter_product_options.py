# Generated by Django 4.1 on 2022-09-01 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-date_added']},
        ),
    ]
