# Generated by Django 2.2.5 on 2019-09-16 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_address_invalid_coordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='floor',
            field=models.IntegerField(blank=True, null=True, verbose_name='этаж'),
        ),
    ]