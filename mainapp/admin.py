# здесь регистрируем свои модели
from django.contrib import admin
from django.utils.html import format_html

from mainapp.models import News, Course, Lesson, CourseTeacher


# admin.site.register(News)  # после того, как сюда зарегистрировали News - при обновлении админки появились новости
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseTeacher)

# Перерегистрируем модель новостей для отображения в админке:
@admin.register(News)  # регистрируем модель, которую хотим использовать
class NewsAdmin(admin.ModelAdmin):  # название модели и где переиспользуем
    list_display = ('pk', 'title', 'slug', 'preamble', 'deleted')  # Это список тех столбцов, который будут выводиться
    # при просмотре списка новостей в админке. ВАЖНО!!! - тут прописываются те поля, которые были в модели либо те,
    # которые мы описали отдельно (ниже def slug...)
    list_filter = ('deleted', 'created_at')  # фильтрация по параметру. Передаём сюда итерируемый объект.
    # В админке появиться новая менюшка с выбором по Удалённым (все, да, нет), По дате создания (любая дата, сегодня,
    # последние 7 дней, месяц, год)
    ordering = ('pk',)  # сортировка по номеру в адмике
    list_per_page = 10  # сколько новостей выводить в адмике
    search_fields = ('title', 'preamble', 'body',)  # поиск по полям. Регистрозависимый. Нужно переписать метод,
    # чтобы поиск не зависел от регистра
    actions = ('mark_as_delete',)  # расширяем стандартные действия с выбранными объектами (новостями). Это список
    # ссылок на функции, на методы, которые мы можем использовать, как действия

    # def slug(self, obj):
    #     """
    #     slug - это отображение адресов страниц, например, новость-из-админки-2
    #     :param obj:
    #     :return:
    #     """
    #     return obj.title.lower().replace(' ', '-')

    def slug(self, obj):
        """
        здесь новости в админке будут открываться в новом окне
        :param obj:
        :return:
        """
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.title.lower().replace(' ', '-'),
            obj.title
        )

    slug.short_description = 'Слаг'  # Кастомноый перевод slug в админке

    # расширяем стандартные действия с выбранными объектами (новостями). Выше мы создавали переменную actions:
    def mark_as_delete(self, request, queryset):  # request - это запрос, queryset - это выбранные новости
        queryset.update(deleted=True)  # обновляем

    mark_as_delete.short_description = 'Пометить удалённым'
