from django.shortcuts import render
from django.http import HttpResponse
# from django.views.generic import View  # Переписываем вьюшки на классы
from django.views.generic import TemplateView


"""
создаём 6 контроллеров для нашего проекта - 6 страниц, каждый из них принимает запрос, 
обрабатывает и выдаёт шаблон, который мы описали в template_name
"""
class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'


class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsView(TemplateView):
    template_name = 'mainapp/news.html'

'''
Это был вводный код 2-го урока:
# вьюшка на классах:
class HelloWorldView(View):  # класс HelloWorldView наследуется от View

    # Описываем поведение для GET-запроса:
    def get(self, request, *args, **kwargs):  # **kwargs - все параметры, которые могут сюда приходитьlf
        """
        классы принимают сам объект self
        :param request: запрос
        :param args: аргументы без ключей
        :param kwargs: аргументы с ключами
        :return: 
        """
        return HttpResponse('Hello world!')

    # Описываем поведение для POST-запроса:  - сейчас не нужен
    # def post(self):
    #     pass

# def hello_world(request):  # переписываем hello_world на классы
#     """
#     Это функция - контроллер - это обработчик, который формирует ответ на запрос.
#     Как до сюда доберётся клиент - переходим в braniaclms/urls.py
#     :param request: - запрос от пользователя
#     :return:
#     """
#     return HttpResponse('Hello world!')


# def blog(request):
#     return HttpResponse('I am blog')


# вьюшка на функциях:
def blog(request, **kwargs):
    """
    Функция контроллер для динамического патерна
    :param request:
    :param kwargs:
    :return:
    """
    return HttpResponse(f'{kwargs}')
'''
