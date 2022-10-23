from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

# app_name = 'mainapp'  # Если не прописали from mainapp.apps import MainappConfig
app_name = MainappConfig.name


urlpatterns = [  # у нас 6 уникальных контролера, если их 1000, то нужно описать 1000
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('courses/', views.CoursesListView.as_view(), name='courses'),
    path('docsite/', views.DocSiteView.as_view(), name='docsite'),
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('news/', views.NewsView.as_view(), name='news'),
    # path('blog/', views.NewsView.as_view(), name='news'),  # если вдруг понадобилось
    # заменить адрес news на blog, мы просто его здесь меняем и всё продолжает работать
    # с новым адресом
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