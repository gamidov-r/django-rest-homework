from django.db import models

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
        blank=True,
        verbose_name="Предосмотр",
        help_text="Загрузите миниатюру",
    )
    video_url = models.TextField(
        blank=True, null=True, verbose_name="Ссылка на видео", help_text="Введите ссылку на видео урока"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
