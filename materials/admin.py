from django.contrib import admin

# Register your models here.
from .models import Course, Lesson

# admin.site.register(User)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_filter = ("name",)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_filter = ("name",)


