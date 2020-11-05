# Generated by Django 2.2.2 on 2019-06-14 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('lat', models.FloatField(blank=True, null=True, verbose_name='широта')),
                ('lon', models.FloatField(blank=True, null=True, verbose_name='долгота')),
                ('is_valid', models.BooleanField(default=True, verbose_name='запись валидна')),
                ('city', models.CharField(max_length=256, null=True, verbose_name='город')),
                ('street', models.CharField(max_length=256, null=True, verbose_name='улица')),
                ('house', models.CharField(max_length=256, null=True, verbose_name='дом')),
                ('building', models.CharField(blank=True, max_length=256, null=True, verbose_name='строение')),
                ('apartment', models.CharField(blank=True, max_length=256, null=True, verbose_name='квартира')),
                ('floor', models.CharField(blank=True, max_length=256, null=True, verbose_name='этаж')),
                ('entrance', models.CharField(blank=True, max_length=256, null=True, verbose_name='подъезд')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий')),
                ('fias_id', models.UUIDField(blank=True, null=True, verbose_name='Идентификатор в ФИАС')),
                ('is_main', models.BooleanField(default=False, verbose_name='основной')),
                ('stop_date', models.DateField(blank=True, default=None, null=True, verbose_name='дата удаления')),
            ],
            options={
                'verbose_name': 'адрес',
                'verbose_name_plural': 'адреса',
            },
        ),
    ]