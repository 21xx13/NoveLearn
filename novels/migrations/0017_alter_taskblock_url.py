# Generated by Django 4.0.2 on 2022-04-17 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0016_taskblock_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskblock',
            name='url',
            field=models.SlugField(null=True, verbose_name='Адрес блока'),
        ),
    ]
