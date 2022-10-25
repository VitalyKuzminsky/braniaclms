# здесь регистрируем свои модели
from django.contrib import admin

from mainapp.models import News

admin.site.register(News)  # после того, как сюда зарегистрировали News - при обновлении админки появились новости

