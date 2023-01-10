from django.core.management import BaseCommand

from mainapp.models import News


class Command(BaseCommand):

    def handle(self, *args, **options):
        new_list = []
        for i in range(10):
            new_list.append(News(
                title=f'title#{i}',
                intro=f'intro#{i}',
                body='some body'
            ))

        News.objects.bulk_create(news_list)
        