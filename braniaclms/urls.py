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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # для редиректа на пустой урл - в корень
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView, - другие
# View, - отвечает за обработку входящего запроса
# TemplateView - отвечает за отображение шаблона

urlpatterns = [
    path('admin/', admin.site.urls),  # Это админка
    path('', RedirectView.as_view(url='mainapp/')),  # редирект с пустого ула на корень сайта.
    # в скобках передаём ардес на который нас редиректить url='mainapp/'
    # Всегда, когда используются классы, как RedirectView нужно передават .as_view,
    # что сделает из неё функцию

    #  т.к. наши ссылки не обображаются из-за того, что мы созали отдельный
    #  модуль mainapp/urls.py нужно их сюда добавить:
    path('mainapp/', include('mainapp.urls'))  # 'mainapp.urls' - путь, где лежат урлы
]
