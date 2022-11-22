from django.db import models
from django.contrib.auth.models import AbstractUser  # Это базовый вариант юзера, в нем все базовые поля

from mainapp.models import NULLABLE


class User(AbstractUser):
    email = models.EmailField(blank=True, verbose_name='Email', unique=True)  # здесь мы переопределяем email - уникаль.
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', **NULLABLE)  # просто число,
    # может быть пустым
    avatar = models.ImageField(upload_to='users', **NULLABLE)  # изображение, может быть пустым

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

