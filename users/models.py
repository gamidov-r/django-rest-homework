from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Ведите почту")
    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name="номер телефона",
        help_text="Введите номер телефона",
    )
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Город", help_text="Укажите Ваш город")
    avatar = models.ImageField(
        upload_to="users/avatars", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите Ваш аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
