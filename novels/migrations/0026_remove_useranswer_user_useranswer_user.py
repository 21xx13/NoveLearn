# Generated by Django 4.0.2 on 2022-04-29 18:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('novels', '0025_remove_useranswer_answers_useranswer_answers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswer',
            name='user',
        ),
        migrations.AddField(
            model_name='useranswer',
            name='user',
            field=models.ManyToManyField(related_name='user_answer', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
