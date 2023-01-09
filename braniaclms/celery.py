# Найстройки Celery
import os
from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "braniaclms.settings")  # Путь к настройкам
celery_app = Celery("braniac")  # Название приложения, которое будем вызывать
celery_app.config_from_object("django.conf:settings", namespace="CELERY")  # Откуда забирается конфигурация
# Celery-приложения
celery_app.autodiscover_tasks()  # автоподгрузка задач
