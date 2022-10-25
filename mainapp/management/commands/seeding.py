# структура собственной консольной команды
from django.core.management import BaseCommand

from mainapp.models import News


class Command(BaseCommand):  # создаём Command, который наследуется от BasCommand, который выше импортировали

    # Command подчеркивало, т.к. нужна имплементация метода handle:
    def handle(self, *args, **options):
        """
        print('ta-da')  # это был пример с выводом в консоль фразы ta-da.
        Далее пишем логику:
        :param args:
        :param options:
        :return:
        """
        news_objects = []
        for i in range(10):  # 1 млн записей делайть не желательно за раз всё-равно, лучше поделить по 100 шт
            news_objects.append(  # здесь мы складываем все новые объекты модели News только в ОЗУ
                News(
                    title=f'news#{i}',
                    preamble=f'preamble#{i}',
                    body=f'Это body для news#{i}'
                )
            )
        News.objects.bulk_create(news_objects)  # здесь будет поднят 1 соединение с БД для всех запросов.
        # bulk_create прнимает список, где лежат созданные объекты

        # for i in range(10):  # такой вариант был слишком затратен по выполнению, т.к. каждое objects.create
        # обращалось к базе и при большом значении n - БД может перестать работать
        #     News.objects.create(
        #         title=f'news#{i}',
        #         preamble=f'preamble#{i}',
        #         body=f'Это body для news#{i}'
        #     )