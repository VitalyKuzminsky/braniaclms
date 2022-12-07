from django.contrib.auth import get_user_model  # чтобы получить ссылку на актуальную модель пользвателя
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

"""
это вместо crispy, который не заработал
"""
class StyleFormMixin:

    def __init__(self, *args, **kwargs):  # когда инициализируется форма - есть работа с полями
        super().__init__(*args, **kwargs)  # вызываем super().__init__ от родительской формы
        for field_name, field in self.fields.items():  # проходимся по списку полей, которые есть
            print(field.widget)
            # делаем проверку чтобы работать с bootstrap'овскими формами
            if isinstance(field.widget, forms.widgets.CheckboxInput):  # если это чек-бокс
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.DateTimeInput):  # если DateTimeInput и т.д.
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-time'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'select2 form-control select2-multiple'
            else:
                field.widget.attrs['class'] = 'form-control'  # обычный селект оборачивается form-control


# Будем описывать форму для регистрации
# class CustomUserCreationForm(StyleFormMixin, UserCreationForm):  # для красоты через StyleFormMixin
class CustomUserCreationForm(UserCreationForm):

    class Meta:  # Обязательно прописываем класс Meta и прописываем 2 обязательных параметра
        # модель:
        model = get_user_model()
        # поля, которые будем заполнять
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'avatar'
        )

    # валидация возраста
    def clean_age(self):  # валидация идёт через clean, потом указывается поле для валидации - age
        age = self.cleaned_data.get('age')  # cleaned_data - это данные внесённые пользователем и отваледированные
        # по базе валидации. Т.е. здесь age - это small integer
        if age < 18:  # сайт для взрослых
            raise ValidationError('Нос не дорос!')
        return age  # Если всё хорошо, возвращаем возраст


# Будем описывать форму для редактирования юзера
class CustomUserChangeForm(UserChangeForm):

    class Meta:  # Обязательно прописываем класс Meta и прописываем 2 обязательных параметра
        # модель:
        model = get_user_model()
        # поля, которые будем заполнять
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'avatar'
        )

    # валидация возраста
    def clean_age(self):  # валидация идёт через clean, потом указывается поле для валидации - age
        age = self.cleaned_data.get('age')  # cleaned_data - это данные внесённые пользователем и отваледированные
        # по базе валидации. Т.е. здесь age - это small integer
        if age < 18:  # сайт для взрослых
            raise ValidationError('Сказано же - сайт для взрослых!')
        return age  # Если всё хорошо, возвращаем возраст
