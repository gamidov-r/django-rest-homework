from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonDetailSerializer(ModelSerializer):
    count_lessons_in_course = serializers.SerializerMethodField()
    def get_count_lessons_in_course(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = ("id", "name", "description", "course", "count_lessons_in_course", )


# class CourseDetailSerializer(ModelSerializer):
#     lessons_in_course = serializers.SerializerMethodField()
#     def get_lessons_in_course(self, lesson):
#         return Lesson.objects.filter(course=lesson.course)
#
#     class Meta:
#         model = Course
#         fields = ("id", "name", "description", "lessons_in_course", )

# TODO
class CourseDetailSerializer(ModelSerializer):
    lessons_course = serializers.SerializerMethodField()
    count_lessons_in_course = serializers.SerializerMethodField()
    def get_count_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_lessons_course(self, course):
        lessons = Lesson.objects.filter(course=course)
        from .serializers import LessonSerializer
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = ("id", "name", "description", "count_lessons_in_course", "lessons_course", )


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
