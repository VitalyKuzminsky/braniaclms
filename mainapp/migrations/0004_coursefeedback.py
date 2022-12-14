# Generated by Django 4.1.2 on 2023-01-06 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mainapp", "0003_alter_courseteacher_options_alter_lesson_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseFeedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.SmallIntegerField(
                        choices=[
                            (5, "⭐⭐⭐⭐⭐"),
                            (4, "⭐⭐⭐⭐"),
                            (3, "⭐⭐⭐"),
                            (2, "⭐⭐"),
                            (1, "⭐"),
                        ],
                        default=5,
                        verbose_name="Рейтинг",
                    ),
                ),
                (
                    "feedback",
                    models.TextField(default="Без отзыва", verbose_name="Отзыв"),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mainapp.course",
                        verbose_name="Курс",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "отзыв",
                "verbose_name_plural": "отзывы",
            },
        ),
    ]
