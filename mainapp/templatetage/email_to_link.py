# Делаем шаблон для адреса электронной почты
from django import template
from django.utils.safestring import mark_safe  # для того, что бы ссылка
# отбражалась на странице не тегом


register = template.Library()  # инициализируем регистратор


@register.filter
def email_to_link(email_string):
    return mark_safe(f"<a href='mailto:{email_string}'>{email_string}</a>")


# вызываем декоратор @register регистр .filter
# Если ничего не передать в фильтр, то он будет называться email_to_link