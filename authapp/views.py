from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from authapp.models import User


# создаём здесь 4 контроллера
# наследуем от TemplateView
class CustomLoginView(LoginView):  # переделываем вход пользователя
    template_name = 'authapp/login.html'
    # ниже пишем атрибут расширения контекста без вызова самого контекста.
    # Это удобно для написания констант
    extra_context = {
        'title': 'Вход пользователя'
    }


class RegisterView(TemplateView):
    template_name = 'authapp/register.html'
    extra_context = {
        'title': 'Регистрация пользователя'
    }

    def post(self, request, *args, **kwargs):  # так как в register.html используем метод отправки post, то здесь
        # нужно его переопределить. У post должно быть много параметров, поэтому раскладываем
        # на и
        try:
            # print(type(request.POST))
            # если все выполняются из набора, то:
            if all(
                    (
                        request.POST.get('username'),  # сама post-форма - это словарь к которому
                            # можно обращаться.
                            # POST-форма лежит в request'е. И затем через get как из обычного
                            # словаря вытаскиваем username и всё остальное
                        request.POST.get('email'),
                        request.POST.get('password1'),
                        request.POST.get('password2'),
                        request.POST.get('first_name'),
                        request.POST.get('last_name'),
                        request.POST.get('password1') == request.POST.get('password2'),
                        # если всё выполняется, то это будет валидацией формы
                    )
            ):
                # то мы создаём пользователя:
                new_user = User.objects.create(
                    username=request.POST.get('username'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    email=request.POST.get('email'),
                    age=request.POST.get('age') if request.POST.get('age') else 0,
                    avatar=request.FILES.get('avatar')
                )
                # print(new_user)  # выводили в консоль юзера
                new_user.set_passowrd(request.POST.get('password1'))  # устанавливаем для нового пользователя пароль
                new_user.save()  # сохраняем нового пользователя
                messages.add_message(request, messages.INFO, 'Регистрация прошла успешно')  # если всё
                # успешно прошло, то берём сообщения и в них отправляем.
                # add_message мы добавляем в request, который у нас есть. Ему обязательно ставим флаг
                # messages.INFO (информируем пользователей) и сообщение
                return HttpResponseRedirect(reverse('authapp:login'))
                # переводим юзера на страницу входа.
                # Соберём через reverse, который лежи в Django
            else:
                messages.add_message(
                    request,
                    messages.WARNING,  # отлавливаем ошибку
                    'Что-то не так с заполненной формой'
                )
        except Exception as ex:
            messages.add_message(
                request,
                messages.WARNING,  # отлавливаем ошибку
                'Что-то пошло не так'
            )
            return HttpResponseRedirect(reverse('authapp:register'))  # возвращаем обратно в регистрацию


class CustomLogoutView(LogoutView):
    pass


class EditView(TemplateView):
    template_name = 'authapp/edit.html'
    extra_context = {
        'title': 'Регистрация пользователя'
    }

    def post(self, request, *args, **kwargs):  # В post`е заполняем все поля, с которыми может работать пользователь.
        if request.POST.get('username'):  # проверка, что что-то передалось в post-форму
            request.user.username = request.POST.get('username')  # request - это метод, в котором храниться инфа
            # какой юзер, откуда пришёл, с каких страниц, что открывалось и тд - т.е. текущий авторизованный юзер,
            # поэтому у юзера можем достать любое поле.

        if request.POST.get('email'):
            request.user.email = request.POST.get('email')

        if request.POST.get('first_name'):
            request.user.first_name = request.POST.get('first_name')

        if request.POST.get('last_name'):
            request.user.last_name = request.POST.get('last_name')

        if request.POST.get('age'):
            request.user.age = request.POST.get('age')

        # if request.POST.get('password'):
        #     request.user.set_password(request.POST.get('password'))  # для пароля испольую специальный метод
        #     # set_password, в которую записывают переменную. Но как правило используют отдельные формы и
        #     # они не соприкасаются с данными юзера. Поэтому здесь закоментируем этот вариант

        request.user.save()  # т.к. тут лежит обычный экземпляр класса, то может вызывать и save.
        return HttpResponseRedirect(reverse('authapp:edit'))  # юзер отредактировал страницу о себе, созранил и
        # вернулся обратно на страницу редактирования.
