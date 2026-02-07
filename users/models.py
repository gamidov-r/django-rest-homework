from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from materials.models import Course, Lesson

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Требуется email адрес")

        email = self.normalize_email(email)

        # if not username:
        #     username = email.split('@')[0]
        #     base_username = username
        #     counter = 1
        #     while User.objects.filter(username=username).exists():
        #         username = f"{base_username}{counter}"
        #         counter += 1

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

    # def get_by_natural_key(self, email):
    #     return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    # username = models.CharField(
    #     max_length=30, unique=True, verbose_name="Имя пользователя", help_text="Используется в качестве логина"
    # )
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
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    PAYMENTS_CHOICES = [("cash", "Наличные"), ("transfer", "Перевод")]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь", help_text="На чье имя платеж"
    )
    payment_date = models.DateField(verbose_name="Дата платежа", help_text="Когда совершен платеж")
    amount = models.FloatField(verbose_name="Сумма", help_text="Оплаченная сумма")
    payment_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Оплаченный курс",
        help_text="За какой курс внесена оплата",
    )
    payment_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Оплаченный урок",
        help_text="За какой урок внесена оплата",
    )
    # payment_type = models.CharField(max_length=50, verbose_name="Тип платежа", help_text="Наличные или перевод")
    payment_type = models.CharField(
        max_length=50, verbose_name="Тип платежа", help_text="Наличные или перевод", choices=PAYMENTS_CHOICES
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]
