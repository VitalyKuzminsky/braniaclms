from django.db import models
# здесть создаём структуру БД


NULLABLE = {'blank': True, 'null': True}


# Создаём аналог таблички новостей
class News(models.Model):  #для этого создаём класс, который наследуется от модуля models и в нём класс Model
    """
    сюда описание модели
    """
    # это то что пойдёт в БД, как отображение таблицы. Далее заносим атрибуты
    title = models.CharField(max_length=256, verbose_name='Заголовок')  # Это типы полей.
    # Все типы полей храняться в пакете models
    preamble = models.CharField(max_length=1024, verbose_name='Вступление')

    body = models.TextField(verbose_name='Содержимое')  # сюда с помощью редактора передаётся html-разметка
    body_as_markdown = models.BooleanField(default=False, verbose_name='Разметка в формате Markdown')  # Это указатель,
    # что нужно выводить или хранить текст в виде markdown - тип разметки,
    # который может использоваться на сайте - преобразование текста в красивам виде.

    # служебные поля:
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    # Каждый раз при создании новост вот это позволяет формировать дату автоматически
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')  # автоматичеки заполняется
    # при обновлении
    deleted = models.BooleanField(default=False, verbose_name='Удалено')  # это поле сообщает удалена запись или нет.
    # Это делается с т.з. безопасности, чтоб не физически удалять инфу, а помечать её, как удалённую

    def __str__(self):
        """
        так же из обязательного в описании модели - нужно переопределить метод str для приведения к строке:
        :return:
        """
        return f'{self.title}'

    # ещё правило хорошего тона задать класс
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'  # plural - множественное число

    # У нашего объекта есть метод delete
    def delete(self, *args, **kwargs):
        """
        метод delete - обозначает, что мы отправим сообщение в БД, что нужно удалить этот объект из базы.
        Но т.к. мы не удаляем совсем, а только помечаем, как удалённое, то нужно переопределить
        метод (он становился True)
        :param args:
        :param kwargs:
        :return:
        """
        self.deleted = True
        self.save()

# для расширения работы с полями прописываем ещё 2 модели: работа с курсами и уроками.
class Course(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')

    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость', default=0)  # DecimalField -
    # число с плавающей . max_digits - это максивальное количество символов в числе
    # до запятой ХХХХХХХХХ и decimal_places после .ХХ По умолчаню стоимость = 0 (default=0)

    # служебные поля копируем такие же:
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')  # мы относимся к какому-то
    # курсу(уроку) и делаем ссылку ч/з ForeignKey. В скобках указывем модель Course и обязательно
    # указать атрибут on_delete с описанием действий, которые нужно делат при удалении
    # курса с уроками. Зачастую каскадно.
    num = models.PositiveIntegerField(default=0, verbose_name='Номер урока')

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return f'#{self.num} {self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        # abstarct = True  # если будет время оптимизировать код, чтобы не повторять создание, обновление,
        # удаление, мета

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


# модель отношения курса к учителям (отношения многим ко многим) - зарезервированные курсы за учителем
class CourseTeacher(models.Model):
    courses = models.ManyToManyField(Course)  # через запись многим ко многим появляется расшивка - она создаётся в БД,
    # как отдельная таблица. Есть таблица отношения учителей к курсам и отношения курса к учителям.
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return f'#{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'курс к учителю'
        verbose_name_plural = 'курсы к учителям'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
