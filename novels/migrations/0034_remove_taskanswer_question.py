# Generated by Django 4.0.2 on 2022-05-13 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0033_usertestslides'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskanswer',
            name='question',
        ),
    ]
