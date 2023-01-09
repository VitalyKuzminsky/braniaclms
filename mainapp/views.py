# from django.views.generic import View  # Переписываем вьюшки на классы
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, DetailView, CreateView, View

from mainapp import tasks
from mainapp.forms import CourseFeedbackForm
# с List по Create это нужно, что бы переделать class NewsView(TemplateView)

from mainapp.models import News, Course, Lesson, CourseTeacher, CourseFeedback

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

    # Обрабатываем post-запрос для отправки формы
    def post(self, *args, **kwargs):
        message_body = self.request.POST.get('message_body')
        message_form = self.request.user.pk if self.request.user.is_authenticated else None
        tasks.send_feedback_mail.delay(message_body, message_form)  # вызываем отложенную задачу delay(отложенный вызов)
        # - добавляем её в очередь, в параметры передаём сообщение и от кого оно пришло.

        return HttpResponseRedirect(reverse_lazy('mainapp:contacts'))


# Вывод курсов:
class CoursesListView(ListView):
    template_name = 'mainapp/courses_list.html'
    model = Course


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


class NewsListView(ListView):
    model = News  # Указываем какую модель используем
    paginate_by = 5  # стандартная настройка отображения количества новостей на странице

    def get_queryset(self):
        """
        Переопределяем get_queryset
        :return: выводим только те новости, которые не помечены, как удалённые deleted=False
        """
        return super().get_queryset().filter(deleted=False)


class NewsDetailView(DetailView):
    model = News

    # Здесь в get_object_or_404() по хорошему нужно отловить ссылки на удалённые новости и выдать 404 ошибку


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'  # Выводим все поля - форма выведет через криспи. Ключевое слово '__all__' - возволяет вывести
    # все поля, которые есть
    success_url = reverse_lazy('mainapp:news')  # редирект на список новостей
    permission_required = ('mainapp.add_news',)  # доступы - объявляем права доступа на добавление новостей, проверяем,
    # что у юзера есть такие права


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'  # Выводим все поля - форма выведет через криспи. Ключевое слово '__all__' - позволяет вывести
    # все поля, которые есть
    success_url = reverse_lazy('mainapp:news')  # редирект на список новостей
    permission_required = ('mainapp.change_news',)  # доступы - объявляем права доступа на изменение новостей,
    # проверяем, что у юзера есть такие права. change_news - эти права создаются автоматически, как только заводим
    # модель.


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


# реализуем контролер для отображаения курса
class CourseDetailView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Описываем получение курса и уроков к нему. Используем метод 404, который может вернуть объект или 404 ошибку.
        # Т.е. она пытается получить из базы объект по фильтрации, который мы передадим, если объекта нет, то он
        # возвращает страницу 404. Если мы не пулучили курс из БД, то 404.
        context_data['course_object'] = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        # Далее получение списка уроков. Без 404 - фильтруем по курсам, который лежи в course_object, т.к.
        # если его там не лежит, то пользователю выкинуло 404 ошибку.
        context_data['lessons'] = Lesson.objects.filter(course=context_data['course_object'])
        # преподаватели
        context_data['teachers'] = CourseTeacher.objects.filter(courses=context_data['course_object'])

        # Для конкретного курса сделаем низкоуровневое кеширование внутри контроллера.
        # Ключ:
        feedback_list_key = f'course_feedback_{context_data["course_object"].pk}'
        # В первую очередь нужно проверить есть ли данные в кеше
        cached_feedback_list = cache.get(feedback_list_key)  # тут уникальный
        # идентификатор курса, который будет отправлять нас на уникальный список фидбеков на этот курс
        # далее проверяем:
        if cached_feedback_list is None:  # если пусто, то:
            context_data['feedback_list'] = CourseFeedback.objects.filter(course=context_data['course_object'])  # из БД
            # выбираем feedback_list, который нам нужен
            # Если было успешно, то передаём ключ и записываем feedback_list в кеш
            cache.set(feedback_list_key, context_data['feedback_list'], timeout=300)  # timeout - время жизни кеша
        # если он есть, то забираем его из кеша
        else:
            context_data['feedback_list'] = cached_feedback_list

        # Вот как я думал - не заработало:
        # context_data['lessons'] = Lesson.course.filter(course=context_data['course_object'])
        # # преподаватели
        # context_data['teachers'] = CourseTeacher.courses.filter(courses=context_data['course_object'])
        # context_data['feedback_list'] = CourseFeedback.course.filter(course=context_data['course_object'])

        # если пользователь авторизован, то будем выводить feedback_form, а собираем её из CourseFeedbackForm
        if self.request.user.is_authenticated:
            context_data['feedback_form'] = CourseFeedbackForm(
                course=context_data['course_object'],
                user=self.request.user
            )

        return context_data


# реализуем контролер для сохранения отзывов на курсы
class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    # ответ будем отправлять из form_valid
    def form_valid(self, form):
        # Форму form, которую приняли в этот метод - мы её сохраняем
        self.object = form.save()
        # Рендерим блок с отзывами с помощью функции render_to_string, которая рендерит строку из указанного шаблона
        # mainapp/includes/feedback_card.html и контекста context=
        rendered_template = render_to_string('mainapp/includes/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_template})


# Контроллер лога
class LogView(UserPassesTestMixin, TemplateView):
    template_name = 'mainapp/logs.html'

    # Делаем, чтобы логи видны были только админу
    def test_func(self):
        return self.request.user.is_superuser  # Если тут будет False, то нам недаст отобразить страницу

    def get_context_data(self, **kwargs):
        # наследуем context_data от родителя, даже если там ничего нет
        context_data = super().get_context_data(**kwargs)
        # список логов
        log_lines = []
        # открываем файл на чтение
        with open(settings.BASE_DIR / 'log/main_log.log') as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:
                    break
                log_lines.insert(0, line)  # такая запись позволяет записывать свежие логи в начало файла

            context_data['logs'] = log_lines
        return context_data


# Контроллер для скачивания логов
class LogDownloadView(UserPassesTestMixin, View):

    # Проверка на админа
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))  # Указываем флаг для чтения в битовом формате "rb"


""" Это всё закомментировал - делаем новости по новому
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
"""

"""class NewsDetail(TemplateView):  # вывод одной конкретной новости
    template_name = 'mainapp/news_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # context_data['object'] = News.objects.get(pk=self.kwargs.get('pk'))  # если ввести в адресной строке номер
        # не существующей новости, то выпадет 500 ошибка (News matching query does not exist.)
        # А надо бы 404 - страница не найдена. Для этого перепишем эту строку:
        context_data['object'] = get_object_or_404(News, pk=self.kwargs.get('pk'))  # get_object_or_404 - это
        # специальная ф-ия, которая принимает модель New и условия фильтрации pk=self.kwargs.get('pk') - условия
        # фильтрации, как правило идёт по первичному ключу
        return context_data"""


'''
Это был вводный код 2-го урока:
# вьюшка на классах:
class HelloWorldView(View):  # класс HelloWorldView наследуется от View

    # Описываем поведение для GET-запроса:
    def get(self, request, *args, **kwargs):  # **kwargs - все параметры, которые могут сюда приходить
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
