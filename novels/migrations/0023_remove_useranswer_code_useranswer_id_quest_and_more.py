# Generated by Django 4.0.2 on 2022-04-29 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('novels', '0022_alter_userslides_read_slides'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswer',
            name='code',
        ),
        migrations.AddField(
            model_name='useranswer',
            name='id_quest',
            field=models.SmallIntegerField(default=0, max_length=32, verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='userslides',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='slides', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
