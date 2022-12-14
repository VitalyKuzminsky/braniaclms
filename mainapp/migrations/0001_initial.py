# Generated by Django 4.1.2 on 2022-10-23 17:16

from django.db import migrations, models


class Migration(migrations.Migration):  # Сама миграция выглядит, как класс, который будет потом вызван
    # и у него будут отрабатываться атрибуты:

    initial = True  # Инициализация миграции, работы с моделью

    dependencies = [  # зависимости миграций. Когда будем создавать слудующие миграции - здесь
        # будут описаны миграция от которой будет зависить эта миграция.
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # id - PRIMARY KEY - эта строка здесь появилась программно
                ('title', models.CharField(max_length=256, verbose_name='Заголовок')),
                ('preamble', models.CharField(max_length=1024, verbose_name='Вступление')),
                ('body', models.TextField(verbose_name='Содержимое')),
                ('body_as_markdown', models.BooleanField(default=False, verbose_name='Разметка в формате Markdown')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Обновлён')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
            ],
            options={
                'verbose_name': 'новость',
                'verbose_name_plural': 'новости',
            },
        ),
    ]
