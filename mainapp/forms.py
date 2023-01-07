from django import forms

from mainapp.models import CourseFeedback


class CourseFeedbackForm(forms.ModelForm):

    class Meta:
        # наша созданная модель
        model = CourseFeedback
        # что отображаем
        fields = ('course', 'user', 'rating', 'feedback',)
        # пользователь и курс должны быть скрыты
        widgets = {
            'course': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            # чтобы рейтинг отображался звёздочками:
            # 'rating': forms.HiddenInput()
        }

    def __init__(self, *args, course=None, user=None, **kwargs):
        """
        Поля course и user принимаем, но мы их не показываем пользователю, поэтому нужно их предустановить через
        метод инициализации. Распаковываем course=None и user=None из **kwargs и по умолчанию они None.
        """
        # Вернувшийся результат возьмём от родителя, который не ожидает от формы ничего, кроме *args, **kwarg:
        super().__init__(*args, **kwargs)
        # проверяем, что юзер и курс в наличии, что они не None, т.о. задали переменные для инициализации форм:
        if course and user:
            self.fields['course'].initial = course.pk
            self.fields['user'].initial = user.pk
