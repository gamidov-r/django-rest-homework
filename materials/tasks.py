import datetime

from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail

from users.models import User


@shared_task
def add():
    print("add hello world")
    return "return hello world"


@shared_task
def check_activity():
    """
    Таска по изменению флага is_active на False всем тем юзерам, которые не заходили более месяца (не 30 дней).
    Сортировка по возрастанию даты. Если цикл дойдет до активного юзера, цикл завершится.
    Запуск запланирован на каждый день.
    """
    last_logins = list(User.objects.values("id", "email", "last_login").order_by("last_login"))
    today = datetime.datetime.now(datetime.timezone.utc)
    for last_login in last_logins:
        if today > last_login["last_login"] + relativedelta(months=1):
            User.objects.get(id=last_login["id"]).update(is_active=False)
        else:
            break
    # чтобы в памяти просто так не висело сутками
    del last_login, today, last_logins  # а то оперативная память дорогая сейчас


@shared_task
def check_subscription():
    """
    Таска по рассылке писем подписанным пользователям на обновление курса
    """
    # вот тут получаем список со словарями пользователей, которые подписаны
    subscribed_users = list(User.objects.filter(subscriptions=1).values("id", "email", "subscriptions"))
    # вот тут кладем в список только адреса электронной почты для дальнейшей рассылки
    emails = list(map(lambda x: x["email"], subscribed_users))

    send_mail(
        "Обновление курса!",
        "Уведомляем Вас, что обновился курс, на который Вы подписаны!\nЕсли это были не Вы, обратитесь в техническую поддержку",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
        fail_silently=False,
    )
    del subscribed_users, emails
