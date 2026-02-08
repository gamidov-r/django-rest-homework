from django.conf import settings
from django.db import models

# from users.models import User


# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Укажите название курса")
    preview = models.ImageField(
        upload_to="materials/course_preview",
        null=True,
        blank=True,
        verbose_name="Предосмотр",
        help_text="Загрузите миниатюру",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание", help_text="Описание курса")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="courses",
        verbose_name="Модератор",
        help_text="Модератор с правами доступа к курсам",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название Урока", help_text="Укажите название урока")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Выберите курс для данного урока",
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание", help_text="Описание урока")
    preview = models.ImageField(
        upload_to="materials/lesson_preview",
        null=True,
        blank=False,
        verbose_name="Предосмотр",
        help_text="Загрузите миниатюру",
    )
    video_url = models.TextField(
        blank=True, null=True, verbose_name="Ссылка на видео", help_text="Введите ссылку на видео урока"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
        verbose_name="Модератор",
        help_text="Модератор с правами доступа к урокам",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    course = models.ForeignKey("materials.Course", on_delete=models.CASCADE, related_name="subscriptions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "subscription"
        verbose_name_plural = "subscriptions"

    def __str__(self):
        return f"{self.user_id} -> {self.course_id}"