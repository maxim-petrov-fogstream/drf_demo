# Generated by Django 2.2.3 on 2019-07-24 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_address_additional_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='invalid_coordinates',
            field=models.BooleanField(default=False),
        ),
    ]
