# Generated by Django 4.1.2 on 2022-12-03 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_course_lesson_courseteacher'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseteacher',
            options={'verbose_name': 'курс к учителю', 'verbose_name_plural': 'курсы к учителям'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'урок', 'verbose_name_plural': 'уроки'},
        ),
    ]
