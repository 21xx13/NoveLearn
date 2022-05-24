# Generated by Django 4.0.2 on 2022-04-15 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0011_alter_taskanswer_correct_text_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('number', models.PositiveSmallIntegerField(default=0, verbose_name='Номер')),
                ('is_code_block', models.BooleanField(default=False, verbose_name='Блок для автопроверки')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novels.taskslide', verbose_name='Слайд')),
            ],
            options={
                'verbose_name': 'Блок теста',
                'verbose_name_plural': 'Блоки теста',
            },
        ),
        migrations.AlterField(
            model_name='taskquestion',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='novels.taskblock', verbose_name='Блок теста'),
        ),
    ]
