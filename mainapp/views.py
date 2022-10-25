# from django.views.generic import View  # Переписываем вьюшки на классы
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from mainapp.models import News

"""
создаём 6 контроллеров для нашего проекта - 6 страниц, каждый из них принимает запрос, 
обрабатывает и выдаёт шаблон, который мы описали в template_name
"""


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    # Создаём вьюшку для емейлов
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['contacts'] = [
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHcrhA',
                'city': 'Санкт‑Петербург',
                'phone': '+7-999-11-11111',
                'email': 'geeklab@spb.ru',
                'address': 'территория Петропавловская крепость, 3Ж',
            },
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHX3xB',
                'city': 'Казань',
                'phone': '+7-999-22-22222',
                'email': 'geeklab@kz.ru',
                'address': 'территория Кремль, 11, Казань, Республика Татарстан, Россия',
            },
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHh9kD',
                'city': 'Москва',
                'phone': '+7-999-33-33333',
                'email': 'geeklab@msk.ru',
                'address': 'Красная площадь, 7, Москва, Россия',
            },
        ]
        return context_data


class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'

    # # переопределяем метод get_context_data у класса
    # def get_context_data(self, **kwargs):  # родительский метод возвражает словарь
    #     context_data = super().get_context_data(**kwargs)
    #     # обращаемся к родителю super(), вызываем у него get_context_data(**kwargs)
    #     context_data['title'] = 'Some title'  # берём новый ключ title и задаём Some title
    #     return context_data  # переопределили родительский метод и вернули результат


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsView(TemplateView):
    template_name = 'mainapp/news.html'

    # так мы делали если нужно создать новость
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['title'] = 'Новость раз'
    #     context_data['preview'] = 'Превью к новости раз'
    #     context_data['date'] = '2022-10-20'
    #     return context_data

    # Если нужно создать набор новостей
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = News.objects.filter(deleted=False)  # прописываем вывод новостей из БД

        # context_data['object_list'] = [  # где каждая новость имеет словарь:
        # ниже устаревший вариант без использования моделей
        # {
        #     'title': 'Новость 1',
        #     'preview': 'Превью к новости 1',
        #     # 'date': datetime.now().strftime('%d.%m.%Y')  # если нужно поменять формат вывода
        #     'date': datetime.now()
        # },
        # {
        #     'title': 'Новость 2',
        #     'preview': 'Превью к новости 2',
        #     'date': datetime.now()
        # },
        # {
        #     'title': 'Новость 3',
        #     'preview': 'Превью к новости 3',
        #     'date': datetime.now()
        # },
        # {
        #     'title': 'Новость 4',
        #     'preview': 'Превью к новости 4',
        #     'date': datetime.now()
        # },
        # {
        #     'title': 'Новость 5',
        #     'preview': 'Превью к новости 5',
        #     'date': datetime.now()
        # },
        # ]
        return context_data


class NewsDetail(TemplateView):  # вывод дной конкретной новости
    template_name = 'mainapp/news_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # context_data['object'] = News.objects.get(pk=self.kwargs.get('pk'))  # если ввести в адресной строке номер
        # не существующей новости, то выпадет 500 ошибка (News matching query does not exist.)
        # А надо бы 404 - страница не найдена. Для этого перепишем эту строку:
        context_data['object'] = get_object_or_404(News, pk=self.kwargs.get('pk'))  # get_object_or_404 - это
        # специальная ф-ия, которая принимает модель New и условия фильтрации pk=self.kwargs.get('pk') - условия
        # фильтрации, как правило идёт по первичому ключу
        return context_data


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
