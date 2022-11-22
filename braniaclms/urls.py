"""braniaclms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # для редиректа на пустой урл - в корень
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView, - другие
# View, - отвечает за обработку входящего запроса
# TemplateView - отвечает за отображение шаблона
from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Это админка
    path('', RedirectView.as_view(url='mainapp/')),  # редирект с пустого ула на корень сайта.
    # в скобках передаём адрес на который нас редиректить url='mainapp/'
    # Всегда, когда используются классы, как RedirectView нужно передават .as_view,
    # что сделает из неё функцию

    #  т.к. наши ссылки не обображаются из-за того, что мы созали отдельный
    #  модуль mainapp/urls.py нужно их сюда добавить:
    path('mainapp/', include('mainapp.urls', namespace='mainapp')),  # 'mainapp.urls' - путь, где лежат урлы
    path('authapp/', include('authapp.urls', namespace='authapp')),  # путь, где лежат урлы авторизации
    path('social_auth/', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:  # импортируем settings из django.conf и проверяем на дебаг DEBUG. Если DEBUG выключен, то
# проект находится на продакшене (продукт готов), он теряет смыл и даже мешает. Поэтому если DEBUG включен, то:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # urlpatterns + static, которая
    # принимает префикс в виде урла, который мы написали в MEDIA_URL мы ищем файлы в этой папке document_root.
    # Теперь Django  умеет работать с медиафайлами.
