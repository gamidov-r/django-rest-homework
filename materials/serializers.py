from rest_framework import serializers
# from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from materials.validators import validate_url, validate_description


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(required=False, allow_null=True, validators=[validate_url])
    description = serializers.CharField(validators=[validate_description])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ("owner",)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class LessonDetailSerializer(serializers.ModelSerializer):
    count_lessons_in_course = serializers.SerializerMethodField()

    def get_count_lessons_in_course(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = (
            "id",
            "name",
            "description",
            "course",
            "count_lessons_in_course",
        )
        read_only_fields = ("owner",)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

# class CourseDetailSerializer(ModelSerializer):
#     lessons_in_course = serializers.SerializerMethodField()
#     def get_lessons_in_course(self, lesson):
#         return Lesson.objects.filter(course=lesson.course)
#
#     class Meta:
#         model = Course
#         fields = ("id", "name", "description", "lessons_in_course")


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_course = serializers.SerializerMethodField()
    count_lessons_in_course = serializers.SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_lessons_course(self, course):
        lessons = Lesson.objects.filter(course=course)
        # from .serializers import LessonSerializer

        return serializers.LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "count_lessons_in_course",
            "lessons_course",
        )


