# Generated by Django 2.2.2 on 2019-07-11 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20190625_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='additional_info',
            field=models.TextField(blank=True, null=True, verbose_name='комментарий'),
        ),
    ]
