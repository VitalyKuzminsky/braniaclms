from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from authapp.forms import CustomUserCreationForm, CustomUserChangeForm
from authapp.models import User


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'Вход пользователя'
    }

class RegisterView(CreateView):
    model = User  # описываем модель
    form_class = CustomUserCreationForm  # написанный перед этим класс в forms.py
    success_url = reverse_lazy('mainapp:index')  # перекидываем на главную страницу после того, как зарегистрировались
    # template_name = 'authapp/register.html'  # ЭТА строка не нужна - делаем через user_form.html

# закоментировали RegisterView, чтобы эту ифу выводить через формы
# class RegisterView(TemplateView):
#     template_name = 'authapp/register.html'
#     extra_context = {
#         'title': 'Регистрация пользователя'
#     }
#
#     def post(self, request, *args, **kwargs):
#         try:
#             if all(
#                     (
#                         request.POST.get('username'),
#                         request.POST.get('email'),
#                         request.POST.get('password_1'),
#                         request.POST.get('password_2'),
#                         request.POST.get('first_name'),
#                         request.POST.get('last_name'),
#                         request.POST.get('password_1') == request.POST.get('password_2'),
#                     )
#             ):
#                 new_user = User.objects.create(
#                     username=request.POST.get('username'),
#                     first_name=request.POST.get('first_name'),
#                     last_name=request.POST.get('last_name'),
#                     email=request.POST.get('email'),
#                     age=request.POST.get('age') if request.POST.get('age') else 0,
#                     avatar=request.FILES.get('avatar'),
#                 )
#                 new_user.set_password(request.POST.get('password_1'))
#                 new_user.save()
#                 messages.add_message(request, messages.INFO, 'Регистрация прошла успешно')
#                 return HttpResponseRedirect(reverse('authapp:login'))
#             else:
#                 messages.add_message(
#                     request,
#                     messages.WARNING,
#                     'Ошибка в Else'
#                 )
#         except Exception as ex:
#             messages.add_message(
#                 request,
#                 messages.WARNING,
#                 'Ошибка в Except'
#             )
#             return HttpResponseRedirect(reverse('authapp:register'))


class CustomLogoutView(LogoutView):
    pass


class EditView(UpdateView):  # для этого контроллера EditView есть апдейт-форма, которая будет отрабатывать.
    # Со стороны html не надо ничего делать, только если хочеться что-то изменить.
    model = User  # описываем модель
    form_class = CustomUserChangeForm
    template_name = 'authapp/edit.html'

    # Если не переопределить get_object, то будет проблема с редактрованием: черзе замену номера юзера мы имеем
    # доступ к редактированию любого юзера http://127.0.0.1:8088/authapp/edit/1/
    def get_object(self, queryset=None):
        return self.request.user  # т.о. куда бы юзер не перешёл, мы будет возвращать именно его

    def get_success_url(self):  # т.к. в urls.py прописано для редактирования edit/<pk>/, то
        # success_url = reverse_lazy('...') не подойдёт. Поэтому мы записываем через метод get_success_url
        return reverse_lazy('authapp:edit', args=[self.request.user.pk])  # получается, что мы передали id текущего
        # пользователя


# закоментировали EditView, чтобы эту ифу выводить через формы
# class EditView(TemplateView):
#     template_name = 'authapp/edit.html'
#     extra_context = {
#         'title': 'Редактирование пользователя'
#     }
#
#     def post(self, request, *args, **kwargs):
#         if request.POST.get('username'):
#             request.user.username = request.POST.get('username')
#
#         if request.POST.get('first_name'):
#             request.user.first_name = request.POST.get('first_name')
#
#         if request.POST.get('last_name'):
#             request.user.last_name = request.POST.get('last_name')
#
#         if request.POST.get('age'):
#             request.user.age = request.POST.get('age')
#
#         if request.POST.get('email'):
#             request.user.email = request.POST.get('email')
#
#         request.user.save()
#         return HttpResponseRedirect(reverse('authapp:edit'))
