from mainapp import views
from django.urls import path
from django.views.decorators.cache import cache_page  # для кеширования импортируем декоратор, который принимает на
# вход значение и функцию, которую будет кешировать
from mainapp.apps import MainappConfig

# app_name = 'mainapp'  # Если не прописали from mainapp.apps import MainappConfig
app_name = MainappConfig.name


urlpatterns = [  # у нас 6 уникальных контролера, если их 1000, то нужно описать 1000
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('docsite/', views.DocSiteView.as_view(), name='docsite'),

    # Courses
    # Курсы будем кешировать. Вызываем cache_page. Передаём на вход время в секундах, views - оборачиваем, как
    # передаваемый параметр
    path('courses/', cache_page(300)(views.CoursesListView.as_view()), name='courses'),
    path('courses/<int:pk>/detail/', views.CourseDetailView.as_view(), name='courses_detail'),
    path('courses/feedback/', views.CourseFeedbackCreateView.as_view(), name='course_feedback'),

    # News
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/add/', views.NewsCreateView.as_view(), name='news_create'),
    # path('news/update/', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name='news_update'),  # <int:pk>, где int -
    # валидация, pk - id.
    path('news/<int:pk>/detail/', views.NewsDetailView.as_view(), name='news_detail'),  # контролер, который выводит отдельные новости
    # path('blog/', views.NewsView.as_view(), name='news'),  # если вдруг понадобилось
    # заменить адрес news на blog, мы просто его здесь меняем и всё продолжает работать
    # с новым адресом
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),

    # Logs
    path('logs/', views.LogView.as_view(), name='logs_list'),
    path('logs/download/', views.LogDownloadView.as_view(), name='logs_download'),
]

'''
Это был вводный код 2-го урока:
urlpatterns = [
    path('', views.HelloWorldView.as_view()),
    # path('', views.hello_world, name='hello_world'),  # это пустой паттерн - он ссылается на корень сайта.
    # Для него импортируем views из mainapp.
    # состав: '' паттерн - первый параментр, передающийся в path
    # views.hello_world - ссылка на ф-ию, которую она быдет отрабатывать
    # name='hello_world' - для быстрого доступа урла - сейчас писать его не будем.
    # path('blog/', views.blog),
    path('<str:word>/', views.blog),  # '<str:word>/' - динамические паттерны ключ:значение
    # любая строка str, которая идёт после корня сайта, будет она будет обращена в .blog
]
'''