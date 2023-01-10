from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse

from authapp.models import User
from mainapp.models import News


# Пишем свой smoke тест - на то что страница открывается
class StaticPagesSmokeTest(TestCase):

    def test_page_index_open(self):
        url = reverse("mainapp:index")  # что тестируем
        result = self.client.get(url)  # записываем результат через свой http client, берём черег get

        # сама проверка результатов:
        self.assertEqual(result.status_code, HTTPStatus.OK)  # сравниваем статус с полученым статусом HTTPStatus.OK=200
        # self.assertEqual(result.status_code, HTTPStatus.BAD_REQUEST)  # "заваливаем тест"

    def test_page_contacts_open(self):
        url = reverse("mainapp:contacts")  # что тестируем
        result = self.client.get(url)  # записываем результат через свой http client, берём черег get

        # сама проверка результатов:
        self.assertEqual(result.status_code, HTTPStatus.OK)  # "заваливаем тест"


# Пишем свой функциональный тест. На то, что простой пользователь не сможет добавить новость
class NewsTestCase(TestCase):

    # Выполняет какие-то команды перед каждым тестом, например, наполнить базу новостями.
    def setUp(self) -> None:
        for i in range(10):
            News.objects.create(
                title=f'News{i}',
                preamble=f'Intro{i}',
                body=f'Body{i}'
            )

        # создаём пользователя
        User.objects.create_superuser(username='django', password='geekbrains')
        self.client_with_auth = Client()
        # Адрес на авторизацию:
        auth_url = reverse('authapp:login')
        # параметры юзера
        self.client_with_auth.post(
            auth_url,
            {
                'username': 'django',
                'password': 'geekbrains'
            }
        )

    # делаем smoke-тест в рамках полноценного тестирования
    def test_open_page(self):
        url = reverse("mainapp:news")
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.OK)

    # тест на провальное открытие неавторизованным юзером страницы редактирования
    def test_failed_open_add_by_anonymous(self):
        url = reverse("mainapp:news_create")
        result = self.client.get(url)

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    # Тест на админа, который создаёт новости
    def test_create_news_item_by_admin(self):

        # проверяем изменилось ли количество новостей до создания
        news_count = News.objects.all().count()

        url = reverse("mainapp:news_create")
        result = self.client_with_auth.post(
            url,
            data={
                'title': 'Test News',
                'preamble': 'Intro',
                'body': 'Body'
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.FOUND)

        # проверяем изменилось ли количество новостей после создания
        self.assertEqual(News.objects.all().count(), news_count + 1)
